from rest_framework import serializers
from django_test_app.jobs.models import Job, JobCategory, JobApplication


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description', 'created_at']


class JobSerializer(serializers.ModelSerializer):
    category = JobCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company_name', 'location',
            'salary_min', 'salary_max', 'status', 'category', 'category_id',
            'created_by_email', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'published_at']
    
    def validate(self, data):
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError({
                'salary_max': 'Maximum salary must be greater than minimum salary'
            })
        
        return data


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'applicant', 'applicant_email',
            'cover_letter', 'resume_url', 'status', 'applied_at', 'reviewed_at'
        ]
        read_only_fields = ['applied_at', 'reviewed_at']

