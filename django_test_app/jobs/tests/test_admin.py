import pytest
from django.contrib.admin.sites import site
from django_test_app.jobs.models import Job, JobCategory, JobApplication
from django_test_app.jobs.tests.factories import JobFactory, JobCategoryFactory
from django_test_app.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestJobAdmin:
    def test_job_admin_registered(self):
        assert site.is_registered(Job)
    
    def test_job_category_admin_registered(self):
        assert site.is_registered(JobCategory)
    
    def test_job_application_admin_registered(self):
        assert site.is_registered(JobApplication)
    
    def test_save_model_sets_created_by(self, admin_user):
        from django_test_app.jobs.admin import JobAdmin
        from django_test_app.jobs.models import Job
        
        admin = JobAdmin(Job, site)
        job = JobFactory.build()
        job.created_by = None
        
        admin.save_model(admin_user, job, None, False)
        assert job.created_by == admin_user

