from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('details/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
]
