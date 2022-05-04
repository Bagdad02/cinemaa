from django.urls import path

from account.views import RegisterApiView, ActivationView, LoginApiView, LogoutView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/',ChangePasswordView.as_view())
]