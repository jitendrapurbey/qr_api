from django.urls import path
from .views import CreateQRView, RegisterUsers, LoginView, SongsDetailView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('create/', CreateQRView.as_view(), name="songs-list-create"),
    path('songs/<int:pk>/', SongsDetailView.as_view(), name="songs-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/logout/', LogoutView.as_view(), name="auth-logout"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('auth/token/', obtain_auth_token, name='auth-token'),

]
