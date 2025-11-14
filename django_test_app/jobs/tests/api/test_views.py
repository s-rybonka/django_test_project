import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django_test_app.jobs.tests.factories import JobFactory, JobCategoryFactory, JobApplicationFactory
from django_test_app.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestJobViewSet:
    def test_list_jobs(self):
        client = APIClient()
        JobFactory(status='published')
        JobFactory(status='published')
        JobFactory(status='draft')
        
        response = client.get('/api/jobs/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_create_job_requires_auth(self):
        client = APIClient()
        category = JobCategoryFactory()
        
        data = {
            'title': 'New Job',
            'description': 'Description',
            'company_name': 'Company',
            'location': 'City',
            'category_id': category.pk,
            'status': 'draft'
        }
        
        response = client.post('/api/jobs/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_job(self):
        client = APIClient()
        user = UserFactory()
        client.force_authenticate(user=user)
        category = JobCategoryFactory()
        
        data = {
            'title': 'New Job',
            'description': 'Description',
            'company_name': 'Company',
            'location': 'City',
            'category_id': category.pk,
            'status': 'draft'
        }
        
        response = client.post('/api/jobs/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Job'
    
    def test_apply_to_job(self):
        client = APIClient()
        user = UserFactory()
        job = JobFactory()
        client.force_authenticate(user=user)
        
        response = client.post(f'/api/jobs/{job.pk}/apply/', {
            'cover_letter': 'I am interested',
            'resume_url': 'http://example.com/resume.pdf'
        })
        
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestJobApplicationViewSet:
    def test_list_applications(self):
        client = APIClient()
        user = UserFactory()
        client.force_authenticate(user=user)
        
        JobApplicationFactory(applicant=user)
        JobApplicationFactory(applicant=user)
        
        response = client.get('/api/applications/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_review_application_requires_staff(self):
        client = APIClient()
        user = UserFactory()
        application = JobApplicationFactory()
        client.force_authenticate(user=user)
        
        response = client.post(f'/api/applications/{application.pk}/review/', {
            'status': 'accepted'
        })
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

