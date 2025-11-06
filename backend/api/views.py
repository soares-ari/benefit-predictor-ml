"""API Views for Benefit Predictor."""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Prediction, EmployeeProfile
from .serializers import (
    PredictionInputSerializer,
    PredictionSerializer,
    PredictionResponseSerializer,
    EmployeeProfileSerializer
)
from .ml.predict import predict_satisfaction

@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'message': 'Benefit Predictor API is running',
        'version': '1.0.0'
    })
@api_view(['POST'])
def predict_view(request):
    """
    Main prediction endpoint.
    
    POST /api/predict/
    Body: {
        "age": 30,
        "salary": 5000.00,
        "commute_time": 45,
        "gym_usage": 12,
        "meal_voucher": 800.00,
        "health_plan_tier": 2
    }
    """
    # Valida input
    input_serializer = PredictionInputSerializer(data=request.data)
    if not input_serializer.is_valid():
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = input_serializer.validated_data

    # Faz predição com ML
    try:
        prediction_result = predict_satisfaction(
            age=int(data['age']),
            salary=float(data['salary']),
            commute_time=int(data['commute_time']),
            gym_usage=int(data['gym_usage']),
            meal_voucher=float(data['meal_voucher']),
            health_plan_tier=int(data['health_plan_tier'])
        )
    except Exception as e:
        return Response(
            {'error': f'Prediction failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Salva no banco
    prediction = Prediction.objects.create(
        age=data['age'],
        salary=data['salary'],
        commute_time=data['commute_time'],
        gym_usage=data['gym_usage'],
        meal_voucher=data['meal_voucher'],
        health_plan_tier=data['health_plan_tier'],
        satisfaction_score=prediction_result['score']
    )

    # Prepara resposta
    response_data = {
        'satisfaction_score': prediction_result['score'],
        'confidence_level': prediction_result['confidence'],
        'recommendation': prediction_result['recommendation'],
        'prediction_id': prediction.id
    }

    response_serializer = PredictionResponseSerializer(data=response_data)
    response_serializer.is_valid(raise_exception=True)

    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de predições.
    
    GET /api/predictions/ - Lista todas
    GET /api/predictions/{id}/ - Detalhes
    GET /api/predictions/stats/ - Estatísticas
    """
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estatísticas gerais."""
        total = Prediction.objects.count()
        avg_score = Prediction.objects.aggregate(Avg('satisfaction_score'))['satisfaction_score__avg']

        return Response({
            'total_predictions': total,
            'average_score': round(avg_score, 2) if avg_score else 0,
            'distribution': {
                'low': Prediction.objects.filter(satisfaction_score__lt=50).count(),
                'medium': Prediction.objects.filter(satisfaction_score__gte=50, satisfaction_score__lt=75).count(),
                'high': Prediction.objects.filter(satisfaction_score__gte=75).count()
            }
        })

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """CRUD para perfis de funcionários."""
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer