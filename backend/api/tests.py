"""
Unit tests for the Benefit Predictor API.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Prediction, EmployeeProfile


@pytest.mark.django_db
class TestHealthCheck(APITestCase):
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that health check returns 200."""
        url = reverse('health-check')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'healthy'
        assert 'version' in response.data


@pytest.mark.django_db
class TestPredictionAPI(APITestCase):
    """Test prediction endpoint."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.predict_url = reverse('predict')
        
        self.valid_payload = {
            'age': 30,
            'salary': 5000.00,
            'commute_time': 45,
            'gym_usage': 12,
            'meal_voucher': 800.00,
            'health_plan_tier': 2
        }
    
    def test_predict_valid_input(self):
        """Test prediction with valid input."""
        response = self.client.post(
            self.predict_url,
            self.valid_payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'satisfaction_score' in response.data
        assert 'confidence_level' in response.data
        assert 'recommendation' in response.data
        assert 'prediction_id' in response.data
        
        # Check score is in valid range
        score = response.data['satisfaction_score']
        assert 0 <= score <= 100
    
    def test_predict_invalid_age(self):
        """Test prediction with invalid age."""
        payload = self.valid_payload.copy()
        payload['age'] = 15  # Too young
        
        response = self.client.post(
            self.predict_url,
            payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_predict_invalid_salary(self):
        """Test prediction with invalid salary."""
        payload = self.valid_payload.copy()
        payload['salary'] = 1000  # Below minimum wage
        
        response = self.client.post(
            self.predict_url,
            payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_predict_missing_field(self):
        """Test prediction with missing required field."""
        payload = self.valid_payload.copy()
        del payload['age']
        
        response = self.client.post(
            self.predict_url,
            payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_prediction_saved_to_database(self):
        """Test that prediction is saved to database."""
        initial_count = Prediction.objects.count()
        
        response = self.client.post(
            self.predict_url,
            self.valid_payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Prediction.objects.count() == initial_count + 1
        
        # Verify saved data
        prediction = Prediction.objects.latest('created_at')
        assert prediction.age == self.valid_payload['age']
        assert float(prediction.salary) == self.valid_payload['salary']
    
    def test_predict_edge_case_max_values(self):
        """Test with maximum valid values."""
        payload = {
            'age': 100,
            'salary': 99999.99,
            'commute_time': 300,
            'gym_usage': 30,
            'meal_voucher': 9999.99,
            'health_plan_tier': 3
        }
        
        response = self.client.post(
            self.predict_url,
            payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_predict_edge_case_min_values(self):
        """Test with minimum valid values."""
        payload = {
            'age': 18,
            'salary': 1320.00,
            'commute_time': 0,
            'gym_usage': 0,
            'meal_voucher': 0.00,
            'health_plan_tier': 1
        }
        
        response = self.client.post(
            self.predict_url,
            payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPredictionViewSet(APITestCase):
    """Test prediction history endpoints."""
    
    def setUp(self):
        """Create test predictions."""
        self.client = APIClient()
        
        # Create sample predictions
        Prediction.objects.create(
            age=30,
            salary=5000,
            commute_time=45,
            gym_usage=12,
            meal_voucher=800,
            health_plan_tier=2,
            satisfaction_score=75.5
        )
        Prediction.objects.create(
            age=45,
            salary=8000,
            commute_time=30,
            gym_usage=20,
            meal_voucher=1000,
            health_plan_tier=3,
            satisfaction_score=85.2
        )
    
    def test_list_predictions(self):
        """Test listing all predictions."""
        url = reverse('prediction-list')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_retrieve_prediction(self):
        """Test retrieving a specific prediction."""
        prediction = Prediction.objects.first()
        url = reverse('prediction-detail', kwargs={'pk': prediction.pk})
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == prediction.id
        assert float(response.data['satisfaction_score']) == prediction.satisfaction_score
    
    def test_stats_endpoint(self):
        """Test statistics endpoint."""
        url = reverse('prediction-stats')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_predictions' in response.data
        assert 'average_score' in response.data
        assert 'distribution' in response.data
        
        assert response.data['total_predictions'] == 2
        assert response.data['average_score'] > 0
        
        # Check distribution structure
        assert 'low' in response.data['distribution']
        assert 'medium' in response.data['distribution']
        assert 'high' in response.data['distribution']


@pytest.mark.django_db
class TestModels(APITestCase):
    """Test model functionality."""
    
    def test_create_prediction(self):
        """Test creating a Prediction instance."""
        prediction = Prediction.objects.create(
            age=35,
            salary=6000,
            commute_time=60,
            gym_usage=15,
            meal_voucher=900,
            health_plan_tier=2,
            satisfaction_score=72.3
        )
        
        assert prediction.id is not None
        assert str(prediction) == f"Previsão {prediction.id} - Score: 72.30"
        assert prediction.age == 35
        assert float(prediction.salary) == 6000
    
    def test_create_employee_profile(self):
        """Test creating an EmployeeProfile instance."""
        profile = EmployeeProfile.objects.create(
            employee_id='EMP001',
            name='Test Employee',
            department='Engineering'
        )
        
        assert profile.id is not None
        assert str(profile) == "Test Employee (EMP001)"
        assert profile.employee_id == 'EMP001'
    
    def test_prediction_ordering(self):
        """Test that predictions are ordered by created_at descending."""
        pred1 = Prediction.objects.create(
            age=30, salary=5000, commute_time=45, gym_usage=12,
            meal_voucher=800, health_plan_tier=2, satisfaction_score=70
        )
        pred2 = Prediction.objects.create(
            age=35, salary=6000, commute_time=30, gym_usage=15,
            meal_voucher=900, health_plan_tier=3, satisfaction_score=80
        )
        
        predictions = list(Prediction.objects.all())
        assert predictions[0].id == pred2.id  # Most recent first
        assert predictions[1].id == pred1.id


@pytest.mark.django_db
class TestEmployeeProfileViewSet(APITestCase):
    """Test employee profile CRUD operations."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = APIClient()
        self.list_url = reverse('employee-list')
        
        self.valid_payload = {
            'employee_id': 'EMP001',
            'name': 'João Silva',
            'department': 'Engineering'
        }
    
    def test_create_employee_profile(self):
        """Test creating an employee profile."""
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['employee_id'] == 'EMP001'
        assert response.data['name'] == 'João Silva'
    
    def test_list_employee_profiles(self):
        """Test listing employee profiles."""
        EmployeeProfile.objects.create(**self.valid_payload)
        
        response = self.client.get(self.list_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_unique_employee_id_constraint(self):
        """Test that employee_id must be unique."""
        EmployeeProfile.objects.create(**self.valid_payload)
        
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST