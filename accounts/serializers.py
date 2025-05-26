

from rest_framework.exceptions import (
    AuthenticationFailed
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()




class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True) 
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }
        
    
    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError("Email is required.")
        email = email.lower()  # normalze email and make it lowercase
        return email

    def validate(self, attrs: dict):
        password = attrs.get('password', None)
        password2 = attrs.pop('password2', None)
        email = attrs.get('email', None)
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")

        if not password or not password2:
            raise serializers.ValidationError("Password is required.")
        if password != password2:
            raise serializers.ValidationError("Password fields didn't match.")
        
        return attrs

    def create(self, validated_data: dict):
        instance =  super().create(validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation




class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    def validate_email(self, email: str):
        email = email.lower()
        return email
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with this email does not exist")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect authentication credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Your account is suspended. Please contact support.")

        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        user: User = self.validated_data.get("user")
        token = TokenObtainPairSerializer.get_token(user)

        representation = {
            "first_name": user.first_name if user.first_name else "",
            "last_name": user.last_name if user.last_name else "",
            "refresh": str(token),
            "access": str(token.access_token),
            "is_onboarded": user.is_onboarded
        }
        return representation


