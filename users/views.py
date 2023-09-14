
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User


class UserViewSet(ModelViewSet):
    serializer_class = User
    queryset = User.objects.all()

    # def update(self, request, *args, **kwargs):
    #     user = self.request.user
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, user=user)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)
