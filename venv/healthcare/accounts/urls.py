from django.urls import path
from .views import register, user_login, user_logout, patient_dashboard, doctor_dashboard

urlpatterns = [
path('register/', register, name='register'),
path('login/', user_login, name='login'),
path('logout/', user_logout, name='logout'),
path('patient_dashboard/', patient_dashboard, name='patient_dashboard'),
path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
]