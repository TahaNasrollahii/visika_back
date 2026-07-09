from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('signup/', views.SignUpView.as_view()),

    path('otp/request/', views.OTPRequestView.as_view()),
    path('otp/login/', views.OTPLoginView.as_view()),
    path('otp/register/', views.OTPRegisterView.as_view()),

    path('info/', views.UserInfoView.as_view(), name='user-info'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/<int:product_id>/toggle/', views.ToggleFavoriteView.as_view(), name='favorite-toggle'),
    path('notifications/', views.NotificationListView.as_view(), name='user-notifications'),
]