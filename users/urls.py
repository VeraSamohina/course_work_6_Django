from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, VerificationEmailView, UserListView, toggle_users_status, \
     UserLoginView

app_name = UsersConfig.name

urlpatterns = [
     path('', UserLoginView.as_view(template_name='users/login.html'), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('register/', RegisterView.as_view(), name='register'),
     path('profile/', UserUpdateView.as_view(), name='profile'),
     path('register/verification/<int:pk>', VerificationEmailView.as_view(), name='verification'),
     path('users/', UserListView.as_view(), name='users'),
     path('toggle_users_status/<int:pk>', toggle_users_status, name='toggle_users_status'),
]
