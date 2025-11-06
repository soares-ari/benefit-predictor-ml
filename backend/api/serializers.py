"""Serializers for the Benefit Predictor API."""
from rest_framework import serializers
from .models import Prediction, EmployeeProfile


class PredictionInputSerializer(serializers.Serializer):
    """Valida dados de entrada para predição."""
    age = serializers.IntegerField(min_value=18, max_value=100)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1320)
    commute_time = serializers.IntegerField(min_value=0, max_value=300)
    gym_usage = serializers.IntegerField(min_value=0, max_value=30)
    meal_voucher = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0)
    health_plan_tier = serializers.IntegerField(min_value=1, max_value=3)


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Prediction."""
    class Meta:
        model = Prediction
        fields = '__all__'
        read_only_fields = ['created_at', 'satisfaction_score']


class PredictionResponseSerializer(serializers.Serializer):
    """Response da API de predição."""
    satisfaction_score = serializers.FloatField()
    confidence_level = serializers.CharField()
    recommendation = serializers.CharField()
    prediction_id = serializers.IntegerField(required=False)


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer para EmployeeProfile."""
    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']