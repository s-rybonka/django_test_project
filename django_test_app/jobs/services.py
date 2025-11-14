from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Job, JobApplication


def publish_job(job_id):
    try:
        job = Job.objects.get(pk=job_id)
        if job.status == 'draft':
            job.status = 'published'
            job.published_at = timezone.now()
            job.save()
            return True
        return False
    except Job.DoesNotExist:
        return False


def close_job(job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.status = 'closed'
        job.save()
        return True
    except Job.DoesNotExist:
        return False


def send_application_notification(application_id):
    application = JobApplication.objects.get(pk=application_id)
    job = application.job
    
    subject = f'New application for {job.title}'
    message = f'You have received a new application from {application.applicant.email} for the position {job.title}.'
    recipient = job.created_by.email
    
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
        [recipient],
        fail_silently=False,
    )


def get_job_statistics(job_id):
    job = Job.objects.get(pk=job_id)
    applications = JobApplication.objects.filter(job=job)
    total_applications = applications.count()
    pending = applications.filter(status='pending').count()
    accepted = applications.filter(status='accepted').count()
    rejected = applications.filter(status='rejected').count()
    
    return {
        'total': total_applications,
        'pending': pending,
        'accepted': accepted,
        'rejected': rejected,
    }


def search_jobs(query, category_id=None, min_salary=None, max_salary=None):
    jobs = Job.objects.filter(status='published')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company_name__icontains=query)
        )
    
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    
    if min_salary:
        jobs = jobs.filter(salary_min__gte=min_salary)
    
    if max_salary:
        jobs = jobs.filter(salary_max__lte=max_salary)
    
    return jobs

