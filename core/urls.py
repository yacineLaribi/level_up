from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.index , name='index'),
    path('login/',views.login_user , name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_view , name='logout'),
    path('chat/', views.chatbot, name='chatbot'),
    path('chatbot/', views.chat_with_bot, name='chat_with_bot'),
    path('profile/', views.profile, name='profile'),
    path('clans/', views.clans, name='clans'),


]
