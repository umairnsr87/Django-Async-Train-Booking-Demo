from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home' ),
    path('profile',views.profile,name='profile' ),
    path('login',views.home,name='login' ),
    path('logout',views.logout_fun,name='logout' ),
    path('register',views.register,name='register' ),

]
