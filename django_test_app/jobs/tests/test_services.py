import pytest
from django.utils import timezone
from django_test_app.jobs.models import Job, JobApplication
from django_test_app.jobs.services import publish_job, close_job, get_job_statistics, search_jobs
from django_test_app.jobs.tests.factories import JobFactory, JobApplicationFactory, JobCategoryFactory


@pytest.mark.django_db
class TestPublishJob:
    def test_publish_draft_job(self):
        job = JobFactory(status='draft')
        result = publish_job(job.pk)
        
        assert result is True
        job.refresh_from_db()
        assert job.status == 'published'
        assert job.published_at is not None
    
    def test_publish_already_published(self):
        job = JobFactory(status='published')
        result = publish_job(job.pk)
        assert result is False


@pytest.mark.django_db
class TestCloseJob:
    def test_close_job(self):
        job = JobFactory(status='published')
        result = close_job(job.pk)
        
        assert result is True
        job.refresh_from_db()
        assert job.status == 'closed'


@pytest.mark.django_db
class TestGetJobStatistics:
    def test_statistics(self):
        job = JobFactory()
        JobApplicationFactory(job=job, status='pending')
        JobApplicationFactory(job=job, status='pending')
        JobApplicationFactory(job=job, status='accepted')
        JobApplicationFactory(job=job, status='rejected')
        
        stats = get_job_statistics(job.pk)
        
        assert stats['total'] == 4
        assert stats['pending'] == 2
        assert stats['accepted'] == 1
        assert stats['rejected'] == 1


@pytest.mark.django_db
class TestSearchJobs:
    def test_search_by_query(self):
        JobFactory(title='Python Developer', status='published')
        JobFactory(title='Java Developer', status='published')
        
        results = search_jobs('Python')
        assert results.count() == 1
        assert results.first().title == 'Python Developer'
    
    def test_search_by_category(self):
        category = JobCategoryFactory()
        JobFactory(category=category, status='published')
        JobFactory(status='published')
        
        results = search_jobs(None, category_id=category.pk)
        assert results.count() == 1

