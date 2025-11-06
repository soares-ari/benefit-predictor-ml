"""
Módulo de predição para o modelo de satisfação.
"""

import os
import joblib
import pandas as pd


# Caminho do modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# Carrega modelo ao importar o módulo
try:
    model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
    print(f"✅ Modelo ML carregado com sucesso!")
except FileNotFoundError:
    model = None
    MODEL_LOADED = False
    print(f"⚠️ Modelo não encontrado em {MODEL_PATH}")
    print("Execute: python api/ml/train_model.py")


def predict_satisfaction(age, salary, commute_time, gym_usage, meal_voucher, health_plan_tier):
    """
    Prediz satisfação do funcionário baseado em benefícios e demográficos.
    
    Args:
        age (int): Idade (18-100)
        salary (float): Salário mensal em BRL
        commute_time (int): Tempo de deslocamento em minutos
        gym_usage (int): Dias/mês usando academia (0-30)
        meal_voucher (float): Valor mensal do vale-refeição em BRL
        health_plan_tier (int): Nível do plano (1=Básico, 2=Padrão, 3=Premium)
    
    Returns:
        dict: {
            'score': float (0-100),
            'confidence': str ('high', 'medium', 'low'),
            'recommendation': str
        }
    """
    if not MODEL_LOADED:
        raise Exception("Modelo não carregado. Execute train_model.py primeiro!")
    
    # Prepara dados como DataFrame (mesmos nomes e ordem do treino!)
    input_data = pd.DataFrame({
        'age': [age],
        'salary': [salary],
        'commute_time': [commute_time],
        'gym_usage': [gym_usage],
        'meal_voucher': [meal_voucher],
        'health_plan_tier': [health_plan_tier]
    })
    
    # Faz predição
    score = model.predict(input_data)[0]
    
    # Garante range válido
    score = max(0, min(100, score))
    
    # Calcula confidence baseado em valores típicos
    confidence = _calculate_confidence(salary, commute_time, gym_usage, health_plan_tier)
    
    # Gera recomendação
    recommendation = _generate_recommendation(score, salary, commute_time, gym_usage, health_plan_tier)
    
    return {
        'score': round(score, 2),
        'confidence': confidence,
        'recommendation': recommendation
    }


def _calculate_confidence(salary, commute_time, gym_usage, health_plan_tier):
    """
    Calcula nível de confiança baseado na razoabilidade dos inputs.
    """
    # Ranges típicos
    typical_ranges = {
        'salary': (2000, 12000),
        'commute': (10, 120),
        'gym': (0, 20),
        'health': (1, 3)
    }
    
    in_range_count = 0
    total_checks = 4
    
    if typical_ranges['salary'][0] <= salary <= typical_ranges['salary'][1]:
        in_range_count += 1
    if typical_ranges['commute'][0] <= commute_time <= typical_ranges['commute'][1]:
        in_range_count += 1
    if typical_ranges['gym'][0] <= gym_usage <= typical_ranges['gym'][1]:
        in_range_count += 1
    if typical_ranges['health'][0] <= health_plan_tier <= typical_ranges['health'][1]:
        in_range_count += 1
    
    confidence_ratio = in_range_count / total_checks
    
    if confidence_ratio >= 0.75:
        return 'high'
    elif confidence_ratio >= 0.5:
        return 'medium'
    else:
        return 'low'


def _generate_recommendation(score, salary, commute_time, gym_usage, health_plan_tier):
    """
    Gera recomendação acionável baseada no score.
    """
    if score >= 80:
        return "Excelente nível de satisfação. Funcionário altamente engajado com os benefícios."
    
    elif score >= 60:
        recommendations = []
        
        if commute_time > 90:
            recommendations.append("considerar home office ou vale-transporte")
        if gym_usage < 5:
            recommendations.append("incentivar uso da academia")
        if health_plan_tier == 1:
            recommendations.append("avaliar upgrade do plano de saúde")
        
        if recommendations:
            return "Boa satisfação, mas pode melhorar: " + "; ".join(recommendations)
        else:
            return "Boa satisfação. Monitorar para manter o nível."
    
    else:
        # Satisfação baixa - identifica problemas principais
        issues = []
        
        if salary < 3000:
            issues.append("ajuste salarial")
        if commute_time > 90:
            issues.append("redução de tempo de deslocamento")
        if gym_usage == 0:
            issues.append("promoção de programas de bem-estar")
        if health_plan_tier == 1:
            issues.append("melhoria do plano de saúde")
        
        if issues:
            return f"Satisfação baixa. Prioridades: {', '.join(issues)}"
        else:
            return "Satisfação baixa detectada. Agendar 1-on-1 para identificar preocupações."


def get_model_info():
    """
    Retorna informações sobre o modelo carregado.
    """
    if not MODEL_LOADED:
        return {'loaded': False, 'message': 'Modelo não encontrado'}
    
    return {
        'loaded': True,
        'model_type': type(model).__name__,
        'features': ['age', 'salary', 'commute_time', 'gym_usage', 'meal_voucher', 'health_plan_tier']
    }