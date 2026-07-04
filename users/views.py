from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from rest_framework.throttling import ScopedRateThrottle

from users.serializers import SignUpSerializer, OTPRequestSerializer, OTPLoginSerializer, UserInfoSerializer, UpdateProfileSerializer
from users.utils import set_tokens_on_cookie
from users.services import OTPService, UserService

User = get_user_model()

class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TypeError as e:
            raise InvalidToken(e.args[0])
        
        output = serializer.validated_data
        response = Response(output, status=status.HTTP_200_OK)
        set_tokens_on_cookie(response, output["access"], output["refresh"])
        
        return response
    

class SignUpView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'anon'
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = UserService.get_tokens_for_user(user)
        response = Response(tokens, status=status.HTTP_201_CREATED)
        set_tokens_on_cookie(response, tokens["access"], tokens["refresh"])

        return response
    

class OTPRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp'

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        
        OTPService.request_otp(phone)

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class OTPLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'anon'

    def post(self, request):
        serializer = OTPLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone = serializer.validated_data['phone_number']
        incoming_otp = serializer.validated_data['otp']
        
        if not OTPService.verify_otp(phone, incoming_otp):
            raise exceptions.ValidationError({"otp": "Invalid or expired OTP"})

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            user = UserService.create_user(phone_number=phone)

        UserService.mark_phone_as_verified(user)
        
        tokens = UserService.get_tokens_for_user(user)
        
        response = Response(tokens, status=status.HTTP_200_OK)
        set_tokens_on_cookie(response, tokens["access"], tokens["refresh"])
        
        return response
    

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = (
            User.objects.prefetch_related("groups")
            .only("id", "phone_number", "first_name", "last_name", "email", "national_id", "birth_date",
                "status", "is_phone_verified")
            .get(id=request.user.id)
        )
        return Response(UserInfoSerializer(user).data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        from users.utils import remove_tokens_from_cookie
        remove_tokens_from_cookie(response)
        return response