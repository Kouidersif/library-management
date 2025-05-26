from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.serializers import CreateUserSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


UserModel = get_user_model()


class AccountsSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ["Accounts API"]


class UserRegisterAPIView(generics.CreateAPIView):
    """
    View for creating users
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer
    queryset = UserModel
    swagger_schema = AccountsSchema

    @swagger_auto_schema(
        operation_description="Create a new user account",
        responses={
            200: openapi.Response(
                description="Registration successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginAPIView(generics.GenericAPIView):
    """
    View for logging in users
    """

    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    swagger_schema = AccountsSchema

    @swagger_auto_schema(
        operation_description="Login with email and password",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_onboarded": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            400: "Bad Request - Invalid credentials",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = AccountsSchema

    @swagger_auto_schema(
        operation_description="Logout and blacklist the refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Bad Request - Invalid token",
            401: "Unauthorized",
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"success": True, "detail": "Token Blacklisted."},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefreshUserTokenAPIView(TokenRefreshView):
    "Custom token refresher to check whether user is active or no before issuing a new token"

    permission_classes = [permissions.AllowAny]
    swagger_schema = AccountsSchema

    @swagger_auto_schema(
        operation_description="Refresh access token and validate user status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Token refresh successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            401: "Unauthorized - Invalid token or inactive user",
        },
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        # Decode the token to get the user ID
        try:
            refresh = RefreshToken(data["refresh"])
            # Attempt to parse the token's user ID
            user_id = refresh["user_id"]
            # Retrieve the user and check if they are active
            user = UserModel.objects.get(id=user_id)
            if not user.is_active:
                return Response(
                    {"error": "User account is disabled."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except (KeyError, UserModel.DoesNotExist, InvalidToken, TokenError):
            return Response(
                {"error": "Invalid token or user does not exist."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
