# Intentional Errors and Suboptimal Solutions in Jobs App

This document tracks all intentional errors and non-optimal but working solutions implemented in the jobs app for code review practice.

## Models (models.py)

1. **Missing validation on salary fields**: No validation to ensure `salary_min < salary_max` when both are provided (validation added in serializer but not in model)
2. **No validation on status transitions**: Job status can be changed from any state to any state without validation (e.g., closed -> draft)
3. **Added index**: Added index on `company_name` but could also add on `location` and other frequently queried fields
4. **No soft delete**: Jobs are hard deleted, no archive functionality
5. **No slug field**: Using integer PKs in URLs instead of slugs for better SEO
6. **Missing model methods**: No custom methods like `is_published()`, `can_apply()`, etc.

## Admin (admin.py)

1. **Inefficient queryset**: No `select_related` or `prefetch_related` optimizations in list views
2. **Missing list_per_page**: Using default pagination which may not be optimal
3. **No custom admin actions for bulk operations**: Only individual actions, no bulk status updates
4. **Missing date_hierarchy**: Could add date_hierarchy for better filtering
5. **No autocomplete_fields**: Foreign key fields don't use autocomplete for better UX

## Views (views.py)

1. **N+1 query problem**: `JobListView` uses `select_related` but could still have issues with related data
2. **No permission checks**: `JobUpdateView` allows any user to edit their own jobs, but no check if job belongs to user in detail view
3. **Missing error handling**: `JobApplicationCreateView.get_job()` could raise DoesNotExist exception
4. **No pagination configuration**: Using default pagination settings
5. **Inefficient search**: Case-insensitive search without proper indexing
6. **Missing form validation**: No custom form validation for business rules

## API Views (api/views.py)

1. **Inefficient queryset**: `JobViewSet.get_queryset()` uses `prefetch_related('applications')` which may not always be needed
2. **Race condition**: `apply` action checks existence then creates, but no transaction or unique constraint handling
3. **Missing pagination class**: Using default pagination
4. **No filtering backend**: Could use django-filter for better filtering
5. **Permission logic issue**: `get_permissions()` method but also has `permission_classes` class attribute - redundant
6. **No rate limiting**: API endpoints don't have rate limiting
7. **Fixed**: Added validation that job status is 'published' before allowing applications
8. **Inefficient status check**: `review` action checks `is_staff` but could use permission classes
9. **Inconsistent permission handling**: `perform_create` checks authentication but permission class should handle it
10. **Import inside method**: `timezone` imported inside `review` method instead of at top

## Serializers (api/serializers.py)

1. **Fixed**: Added validation for salary ranges in `validate` method
2. **No nested writes**: Category can only be set by ID, not by nested object
3. **Missing field validation**: No validation that resume_url is a valid URL format
4. **No custom to_representation**: Could optimize serialization output
5. **Missing related field optimization**: Using `source` for related fields instead of SerializerMethodField for better control
6. **Field name inconsistency**: Using both `category_id` as field name and write_only parameter - could be clearer

## Services (services.py)

1. **No error handling**: `publish_job` and `close_job` now have try/except but could use better error messages
2. **Missing transaction management**: No `@transaction.atomic` decorators for operations that should be atomic
3. **Email sending without async**: `send_application_notification` sends email synchronously, should use Celery
4. **Missing logging**: No logging for important operations
5. **Inefficient queries**: `get_job_statistics` makes multiple queries instead of using aggregation
6. **No caching**: Statistics and search results could be cached
7. **Missing validation**: `search_jobs` doesn't validate input parameters
8. **Settings access**: Using `getattr` for DEFAULT_FROM_EMAIL but should be in settings validation

## Tests

1. **test_models.py**:
   - Fixed: `test_unique_together` had undefined variable `application`
   - Missing edge cases: No tests for invalid data, boundary conditions
   - No integration tests: Only unit tests, no integration tests

2. **test_views.py**:
   - Missing test coverage: Not all view methods are tested
   - No test for error cases: Missing tests for 404, permission denied, etc.
   - Hard-coded URLs: Using reverse() but could test URL patterns

3. **test_admin.py**:
   - Minimal test coverage: Only basic registration tests
   - No test for admin actions: Actions like `mark_as_reviewed` not tested

4. **test_services.py**:
   - No mocking: Email sending not mocked in tests
   - Missing edge cases: No tests for DoesNotExist exceptions
   - No performance tests: No tests for query efficiency

5. **test_api/test_views.py**:
   - Missing authentication tests: Not all auth scenarios covered
   - No test for pagination: Pagination not tested
   - Missing filter tests: Query parameter filtering not fully tested

## URLs (urls.py)

1. **No trailing slash consistency**: Some URLs have trailing slashes, some don't
2. **Missing URL namespacing**: Already using app_name, but could be more consistent
3. **No regex patterns**: Using simple path converters, could use regex for validation

## General Issues

1. **No migrations file**: Need to run `makemigrations` to create migration files
2. **Missing templates**: Views reference templates that don't exist
3. **No forms.py**: Using model forms directly in views instead of custom forms
4. **Missing signals**: No signals for post_save, pre_save hooks (e.g., auto-send notifications)
5. **No management commands**: Could have commands for bulk operations, data migration
6. **Missing documentation**: No docstrings for complex methods
7. **No type hints**: Missing type hints in many places
8. **Inconsistent error handling**: Some places use exceptions, others return None/False
9. **No constants file**: Magic strings like 'published', 'draft' should be constants
10. **Missing validation mixins**: Could use DRF validators or Django form validation

