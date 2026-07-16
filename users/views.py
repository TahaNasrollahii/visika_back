from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from rest_framework.throttling import ScopedRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from users.serializers import SignUpSerializer, OTPRequestSerializer, OTPLoginSerializer, OTPRegisterSerializer, UserInfoSerializer, UpdateProfileSerializer
from users.utils import set_tokens_on_cookie
from users.services import OTPService, UserService

User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
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
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
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
        action = request.data.get('action')
        
        if action == 'login':
            if not User.objects.filter(phone_number=phone).exists():
                raise exceptions.NotFound({"detail": "کاربری با این شماره یافت نشد."})
        elif action == 'register':
            if User.objects.filter(phone_number=phone).exists():
                raise exceptions.ValidationError({"phone_number": "کاربری با این شماره از قبل وجود دارد."})
        
        OTPService.request_otp(phone)

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
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
            raise exceptions.NotFound({"detail": "کاربری با این شماره یافت نشد. لطفا ثبت نام کنید."})

        UserService.mark_phone_as_verified(user)
        
        tokens = UserService.get_tokens_for_user(user)
        
        response = Response(tokens, status=status.HTTP_200_OK)
        set_tokens_on_cookie(response, tokens["access"], tokens["refresh"])
        
        return response
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class OTPRegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'anon'

    def post(self, request):
        serializer = OTPRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone = serializer.validated_data['phone_number']
        incoming_otp = serializer.validated_data['otp']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        role = serializer.validated_data['role']
        brand_name = serializer.validated_data.get('brand_name')

        if not OTPService.verify_otp(phone, incoming_otp):
            raise exceptions.ValidationError({"otp": "Invalid or expired OTP"})

        try:
            user = User.objects.get(phone_number=phone)
            # If user exists, just return error or log them in? 
            # The prompt says register page is for new users.
            raise exceptions.ValidationError({"phone_number": "User already exists"})
        except User.DoesNotExist:
            user = UserService.create_user(phone_number=phone)
            user.first_name = first_name
            user.last_name = last_name
            
            if role == User.RoleChoices.VENDOR:
                user.status = User.StatusChoices.PENDING
                user.requested_brand_name = brand_name
            else:
                user.status = User.StatusChoices.ACTIVE
                
            user.role = role
            user.save()

        UserService.mark_phone_as_verified(user)
        
        tokens = UserService.get_tokens_for_user(user)
        
        response = Response(tokens, status=status.HTTP_201_CREATED)
        set_tokens_on_cookie(response, tokens["access"], tokens["refresh"])
        
        return response
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = (
            User.objects.prefetch_related("groups")
            .only("id", "phone_number", "first_name", "last_name", "email", "national_id",
                "status", "role", "is_phone_verified")
            .get(id=request.user.id)
        )
        return Response(UserInfoSerializer(user).data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        from users.utils import remove_tokens_from_cookie
        remove_tokens_from_cookie(response)
        return response

from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import generics

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(id=product_id)
            if user.favorites.filter(id=product_id).exists():
                user.favorites.remove(product)
                return Response({'status': 'removed', 'message': 'Removed from favorites'}, status=status.HTTP_200_OK)
            else:
                user.favorites.add(product)
                return Response({'status': 'added', 'message': 'Added to favorites'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.favorites.all()


from rest_framework import viewsets
from rest_framework.decorators import action
from users.models import Address
from users.serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        address = self.get_object()
        address.is_default = True
        address.save()
        return Response({'status': 'address set to default'})

from users.models import Notification
from users.serializers import UserNotificationSerializer

class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


class UnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread_count": count})


class MarkNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"})