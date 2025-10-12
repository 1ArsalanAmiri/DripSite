from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ...models import User

class UserSerializer(serializers.ModelSerializer):
    permission_classes = (IsAdminUser)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'email', 'created_date' ]
