from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Job, JobApplication


class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Job.objects.filter(status='published')
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(company_name__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return Job.objects.filter(status='published')


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'company_name', 'location', 'salary_min', 'salary_max', 'category', 'status']
    success_url = reverse_lazy('jobs:list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Job created successfully!')
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'company_name', 'location', 'salary_min', 'salary_max', 'category', 'status']
    success_url = reverse_lazy('jobs:list')
    
    def get_queryset(self):
        return Job.objects.filter(created_by=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    template_name = 'jobs/application_form.html'
    fields = ['cover_letter', 'resume_url']
    success_url = reverse_lazy('jobs:list')
    
    def get_job(self):
        job_id = self.kwargs.get('job_id')
        return Job.objects.get(pk=job_id)
    
    def form_valid(self, form):
        form.instance.job = self.get_job()
        form.instance.applicant = self.request.user
        messages.success(self.request, 'Application submitted successfully!')
        return super().form_valid(form)


class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

