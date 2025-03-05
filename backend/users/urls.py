from django.contrib import admin
from django.urls import path, include


from users.views import (
    Register, 
    Login, 
    Logout, 
    PasswordResetUpdate, 
    passwordResetRequest)

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('recover/link', passwordResetRequest),
    path('recover/update', PasswordResetUpdate.as_view()),
]
