# drf-nested-decorator

A decorator that allows view actions to be nested (only 1 level - this covers all of my use cases).

I didn't try to create a lot of new stuff, I just edited the SimpleRouter and added a decorator

**Use at own risk.** No tests yet! 'Works for me' though.. :)

I've created this functionality because i was in need, and will try to add tests and better organisation to it when i have time.
Want to use it? Star so i know there's someone else besides me that will benefit from my efforts.

## Usage

my_app/views.py

    from drf_nested_decorator.decorator import nested_detail_route
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from my_users.permission_classes import ActuallyOwnsCard, IsAwesome
    from my_users.serializers import CardSerializer
    from my_users.models import Card
    
    class MyUserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
                       
        authentication_classes = (SessionAuthentication, )
        permission_classes = (IsAuthenticated, )
        queryset = MyUser.objects.all()
        serializer_class = MyUserSerializer
        
        
        @nested_detail_route(['DELETE'], url_path='cards', permission_classes=(IsAwesome, ActuallyOwnsCard) + permission_classes)
        def nested_cards(self, request, pk=None, nested_pk=None)
            serializer = CardSerializer(Card.objects.get(pk=nested_pk))
            return Response(serializer.data)

urls.py

    from drf_nested_decorator.routers import NestedDecoratorSimpleRouter
    from my_app.views import MyUserViewSet
    
    router = NestedDecoratorSimpleRouter()
    router.register(r'myuser', MyUserViewSet, base_name="myuser")


## To do:

- Add tests, for everything (no decorator tests in DRF found, find or create)
- Test with other packages like drf-nested-routers and drf-extensions
- No formal parameter nested_lookup on decorated method supplied ->> good error message
- Find out from what lower version this is supported, I'm using 3.1.3.
- Automatic lookup of nested model through a nested_queryset?
