# drf-nested-decorator

A decorator that allows view actions to be nested and seeks to be integrated into DRF after proper tests are written.

I didn't try to create a lot of new stuff, i just edited the SimpleRouter and added a decorator

**Warning: No tests yet!**

I've created this functionality because i was in need, and will try to add tests and better organisation to it when i have time.
Want to use it? Star so i know there's someone else besides me that will benefit from my efforts.

## Usage

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

## To do:

- Add tests, for everything (no decorator tests in DRF found, find or create)
- Test with other packages like drf-nested-routers and drf-extensions
- No formal parameter nested_lookup on decorated method supplied ->> good error message
- Find out from what lower version this is supported, I'm using 3.1.3.
- Automatic lookup of nested model through a nested_queryset?
