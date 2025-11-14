import pytest
from django_test_app.jobs.models import Job, JobCategory, JobApplication
from django_test_app.jobs.tests.factories import JobFactory, JobCategoryFactory, JobApplicationFactory


@pytest.mark.django_db
class TestJobCategory:
    def test_str(self):
        category = JobCategoryFactory(name="Software Engineering")
        assert str(category) == "Software Engineering"
    
    def test_creation(self):
        category = JobCategoryFactory()
        assert category.pk is not None
        assert category.name is not None


@pytest.mark.django_db
class TestJob:
    def test_str(self):
        job = JobFactory(title="Python Developer", company_name="Tech Corp")
        assert "Python Developer" in str(job)
        assert "Tech Corp" in str(job)
    
    def test_creation(self):
        job = JobFactory()
        assert job.pk is not None
        assert job.title is not None
        assert job.status == 'published'
    
    def test_default_status(self):
        job = JobFactory(status='draft')
        assert job.status == 'draft'


@pytest.mark.django_db
class TestJobApplication:
    def test_str(self):
        application = JobApplicationFactory()
        assert application.applicant.email in str(application)
        assert application.job.title in str(application)
    
    def test_unique_together(self):
        job = JobFactory()
        application = JobApplicationFactory()
        applicant = application.applicant
        
        JobApplicationFactory(job=job, applicant=applicant)
        
        with pytest.raises(Exception):
            JobApplicationFactory(job=job, applicant=applicant)
    
    def test_default_status(self):
        application = JobApplicationFactory()
        assert application.status == 'pending'

