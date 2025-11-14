from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django_test_app.users.api.views import UserViewSet
from django_test_app.jobs.api.views import JobViewSet, JobCategoryViewSet, JobApplicationViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("jobs", JobViewSet)
router.register("categories", JobCategoryViewSet)
router.register("applications", JobApplicationViewSet)


app_name = "api"
urlpatterns = router.urls
