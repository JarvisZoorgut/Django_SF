from django.urls import path
from .views import SignUp
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/templates/registration/login.html'), name='login'),
]