from django.urls import path
from .views import (
    JobListView, JobDetailView, JobCreateView, JobUpdateView,
    JobApplicationCreateView, MyApplicationsListView
)

app_name = 'jobs'
urlpatterns = [
    path('', JobListView.as_view(), name='list'),
    path('<int:pk>/', JobDetailView.as_view(), name='detail'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='edit'),
    path('<int:job_id>/apply/', JobApplicationCreateView.as_view(), name='apply'),
    path('my-applications/', MyApplicationsListView.as_view(), name='my_applications'),
]

