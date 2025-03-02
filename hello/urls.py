from django.urls import path
from . import views

app_name = 'hello'

urlpatterns = [
    path('', views.sessfun),
    path('cookie/', views.cookie, name='cookie'),
    # path('sessfun', views.sessfun, name='session_fun'),
    ]