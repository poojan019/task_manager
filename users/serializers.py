from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[MinLengthValidator(8)]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'role': {'required': True},
        }
    
    def create(self, validated_data):
        validated_data.setdefault('role', 'EMPLOYEE')
        user = User.objects.create_user(**validated_data)
        return user

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']