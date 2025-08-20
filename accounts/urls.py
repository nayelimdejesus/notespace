from django.urls import path
from . import views 
from .views import LoginView
urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.auth_logout, name = 'logout')
]
