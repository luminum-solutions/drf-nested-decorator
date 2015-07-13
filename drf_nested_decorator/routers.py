from rest_framework.routers import SimpleRouter, Route, DynamicDetailRoute, DynamicListRoute, flatten
from django.core.exceptions import ImproperlyConfigured
from collections import namedtuple
from django.conf.urls import url, patterns

DynamicNestedDetailRoute = namedtuple('DynamicNestedDetailRoute', ['url', 'name', 'initkwargs'])


def replace_methodname(format_string, methodname):
    """
    Partially format a format_string, swapping out any
    '{methodname}' or '{methodnamehyphen}' components.
    """
    methodnamehyphen = methodname.replace('_', '-')
    ret = format_string
    ret = ret.replace('{methodname}', methodname)
    ret = ret.replace('{methodnamehyphen}', methodnamehyphen)
    if 'nested_lookup' in format_string:
        ret = ret.replace('{nested_lookup}', '(?P<nested_pk>[^/.]+)')
    return ret


class NestedDecoratorSimpleRouter(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        DynamicNestedDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}/{nested_lookup}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

    def get_routes(self, viewset):
        """
        Augment `self.routes` with any dynamically generated routes.

        Returns a list of the Route namedtuple.
        """

        known_actions = flatten([route.mapping.values() for route in self.routes if isinstance(route, Route)])

        # Determine any `@detail_route` or `@list_route` decorated methods on the viewset
        detail_routes = []
        nested_detail_routes = []
        list_routes = []
        for methodname in dir(viewset):
            attr = getattr(viewset, methodname)
            httpmethods = getattr(attr, 'bind_to_methods', None)
            detail = getattr(attr, 'detail', True)
            nested_detail = getattr(attr, 'nested_detail', False)  # Changed
            if httpmethods:
                if methodname in known_actions:
                    raise ImproperlyConfigured('Cannot use @detail_route or @list_route '
                                               'decorators on method "%s" '
                                               'as it is an existing route' % methodname)
                httpmethods = [method.lower() for method in httpmethods]
                if nested_detail:
                    nested_detail_routes.append((httpmethods, methodname))
                elif detail:
                    detail_routes.append((httpmethods, methodname))
                else:
                    list_routes.append((httpmethods, methodname))

        def _get_dynamic_routes(route, dynamic_routes):
            ret = []
            for httpmethods, methodname in dynamic_routes:
                method_kwargs = getattr(viewset, methodname).kwargs
                initkwargs = route.initkwargs.copy()
                initkwargs.update(method_kwargs)
                url_path = initkwargs.pop("url_path", None) or methodname
                ret.append(Route(
                    url=replace_methodname(route.url, url_path),
                    mapping=dict((httpmethod, methodname) for httpmethod in httpmethods),
                    # As a class cannot have two identically named methods but the url_path should remain equal,
                    # set the name of the route (to be reversed) to the methodname if it's a nested route.
                    name=replace_methodname(route.name, methodname if 'nested_lookup' in route.url else url_path),
                    initkwargs=initkwargs
                ))
            return ret

        ret = []
        for route in self.routes:
            if isinstance(route, DynamicDetailRoute):
                # Dynamic detail routes (@detail_route decorator)
                ret += _get_dynamic_routes(route, detail_routes)
            elif isinstance(route, DynamicNestedDetailRoute):
                # Dynamic detail routes (@nested_detail_route decorator)
                ret += _get_dynamic_routes(route, nested_detail_routes)
            elif isinstance(route, DynamicListRoute):
                # Dynamic list routes (@list_route decorator)
                ret += _get_dynamic_routes(route, list_routes)
            else:
                # Standard route
                ret.append(route)
        return ret