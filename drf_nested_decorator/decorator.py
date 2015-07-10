def nested_detail_route(methods=None, **kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for detail requests.
    """
    methods = ['get'] if (methods is None) else methods

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = True
        func.nested_detail = True  # CHANGED
        func.kwargs = kwargs
        return func

    return decorator
