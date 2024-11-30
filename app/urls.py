from django.urls import path
from app.views import call_execution, get_history, login, register, home, logout

app_name = 'app'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('call/', call_execution, name='call_execution'),
    path('history/', get_history, name='history'),
    path('', home, name='home')
]