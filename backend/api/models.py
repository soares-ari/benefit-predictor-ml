"""
Models for the Benefit Predictor API.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Prediction(models.Model):
    """
    Armazena previsões de satisfação de funcionários.
    Cada registro representa uma predição única com os dados de entrada
    e o score calculado pelo modelo ML.
    """
    # Dados do funcionário
    age = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        help_text="Idade do funcionário"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Salário mensal em EUR"
    )
    commute_time = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Tempo de deslocamento diário em minutos"
    )
    gym_usage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="Dias por mês usando academia"
    )
    meal_voucher = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Valor mensal do vale-refeição em EUR"
    )
    health_plan_tier = models.IntegerField(
        choices=[(1, 'Básico'), (2, 'Padrão'), (3, 'Premium')],
        default=2,
        help_text="Nível do plano de saúde"
    )
    
    # Resultado da predição
    satisfaction_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score de satisfação previsto (0-100)"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Previsão'
        verbose_name_plural = 'Previsões'
    
    def __str__(self):
        return f"Previsão {self.id} - Score: {self.satisfaction_score:.2f}"


class EmployeeProfile(models.Model):
    """
    Perfil de funcionário (opcional - para tracking ao longo do tempo).
    """
    employee_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Perfil de Funcionário'
        verbose_name_plural = 'Perfis de Funcionários'
    
    def __str__(self):
        return f"{self.name} ({self.employee_id})"