import pytest
from django.urls import reverse
from django_test_app.jobs.tests.factories import JobFactory, JobCategoryFactory, JobApplicationFactory
from django_test_app.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestJobListView:
    def test_list_view(self, client):
        JobFactory(status='published')
        JobFactory(status='published')
        JobFactory(status='draft')
        
        response = client.get(reverse('jobs:list'))
        assert response.status_code == 200
        assert len(response.context['jobs']) == 2
    
    def test_search(self, client):
        JobFactory(title='Python Developer', status='published')
        JobFactory(title='Java Developer', status='published')
        
        response = client.get(reverse('jobs:list'), {'search': 'Python'})
        assert response.status_code == 200
        assert len(response.context['jobs']) == 1


@pytest.mark.django_db
class TestJobDetailView:
    def test_detail_view(self, client):
        job = JobFactory(status='published')
        response = client.get(reverse('jobs:detail', kwargs={'pk': job.pk}))
        assert response.status_code == 200
        assert response.context['job'] == job
    
    def test_draft_not_visible(self, client):
        job = JobFactory(status='draft')
        response = client.get(reverse('jobs:detail', kwargs={'pk': job.pk}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestJobCreateView:
    def test_create_requires_login(self, client):
        response = client.get(reverse('jobs:create'))
        assert response.status_code == 302
    
    def test_create_job(self, client):
        user = UserFactory()
        client.force_login(user)
        category = JobCategoryFactory()
        
        data = {
            'title': 'New Job',
            'description': 'Job description',
            'company_name': 'Company',
            'location': 'City',
            'category': category.pk,
            'status': 'draft'
        }
        
        response = client.post(reverse('jobs:create'), data)
        assert response.status_code == 302
        assert Job.objects.filter(title='New Job').exists()


@pytest.mark.django_db
class TestJobApplicationCreateView:
    def test_apply_requires_login(self, client):
        job = JobFactory()
        response = client.get(reverse('jobs:apply', kwargs={'job_id': job.pk}))
        assert response.status_code == 302
    
    def test_create_application(self, client):
        user = UserFactory()
        job = JobFactory()
        client.force_login(user)
        
        data = {
            'cover_letter': 'I am interested',
            'resume_url': 'http://example.com/resume.pdf'
        }
        
        response = client.post(reverse('jobs:apply', kwargs={'job_id': job.pk}), data)
        assert response.status_code == 302
        assert JobApplication.objects.filter(job=job, applicant=user).exists()

