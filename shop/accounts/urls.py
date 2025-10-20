from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('registration/',views.register_view,name='registration'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile_view,name='profile'),
    path('activation-required/', views.activate_account, name='activation-required'),
    path('generation_code/', views.get_confirm_code, name='get_confirm_code'),
  ]