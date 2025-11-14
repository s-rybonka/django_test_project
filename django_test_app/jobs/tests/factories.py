import factory
from factory.django import DjangoModelFactory
from django_test_app.users.tests.factories import UserFactory
from django_test_app.jobs.models import Job, JobCategory, JobApplication


class JobCategoryFactory(DjangoModelFactory):
    class Meta:
        model = JobCategory
    
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker('text', max_nb_chars=200)


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job
    
    title = factory.Faker('job')
    description = factory.Faker('text', max_nb_chars=1000)
    company_name = factory.Faker('company')
    location = factory.Faker('city')
    salary_min = factory.Faker('random_int', min=30000, max=50000)
    salary_max = factory.Faker('random_int', min=50000, max=100000)
    status = 'published'
    category = factory.SubFactory(JobCategoryFactory)
    created_by = factory.SubFactory(UserFactory)


class JobApplicationFactory(DjangoModelFactory):
    class Meta:
        model = JobApplication
    
    job = factory.SubFactory(JobFactory)
    applicant = factory.SubFactory(UserFactory)
    cover_letter = factory.Faker('text', max_nb_chars=500)
    resume_url = factory.Faker('url')
    status = 'pending'

