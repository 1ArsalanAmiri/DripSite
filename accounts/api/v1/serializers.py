from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ...models import User

class UserSerializer(serializers.ModelSerializer):
    permission_classes = (IsAdminUser,)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'gender' ,'email', 'created_date' ]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "email"]


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", required=True, allow_blank=False)
    code = serializers.CharField(max_length=6, label="Code", required=True, allow_blank=False)
