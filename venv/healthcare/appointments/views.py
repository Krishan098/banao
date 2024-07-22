from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment
from .forms import AppointmentForm
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'path/to/service-account-file.json'

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'appointments/doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            start_datetime = datetime.combine(appointment.date, appointment.start_time)
            appointment.end_time = (start_datetime + timedelta(minutes=45)).time()
            appointment.save()
            create_calendar_event(appointment)
            return redirect('appointment_details', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointments/appointment_details.html', {'appointment': appointment})

def create_calendar_event(appointment):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    start_datetime = datetime.combine(appointment.date, appointment.start_time)
    end_datetime = start_datetime + timedelta(minutes=45)

    event = {
        'summary': f'Appointment with {appointment.doctor.user.get_full_name()}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'UTC',
        },
    }

    service.events().insert(calendarId='primary', body=event).execute()
def patient_dashboard(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient_dashboard.html', {'doctors': doctors})