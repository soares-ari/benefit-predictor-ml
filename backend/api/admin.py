"""
Admin configuration for Benefit Predictor API.
"""
from django.contrib import admin
from .models import Prediction, EmployeeProfile


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Interface admin para Predictions."""
    list_display = ['id', 'age', 'salary', 'satisfaction_score', 'created_at']
    list_filter = ['health_plan_tier', 'created_at']
    search_fields = ['id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    """Interface admin para Employee Profiles."""
    list_display = ['employee_id', 'name', 'department', 'created_at']
    list_filter = ['department']
    search_fields = ['employee_id', 'name', 'department']
    readonly_fields = ['created_at', 'updated_at']