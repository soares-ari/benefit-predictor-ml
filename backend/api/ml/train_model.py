"""
Script para treinar o modelo de predição de satisfação.

Este script:
1. Gera dados sintéticos de funcionários
2. Treina um modelo Random Forest
3. Avalia a performance
4. Salva o modelo treinado em model.pkl
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

def generate_synthetic_data(n_samples=2000):
    """
    Gera dados sintéticos de funcionários e satisfação.

    Por que dados sintéticos?
    - Para MVP, não temos dados reais
    - Simula padrões realistas
    - Permite treinar e testar rapidamente

    Args:
        n_samples: Número de exemplos a gerar
    Returns:
        DataFrame com features e target
    """
    np.random.seed(42) # Para resultados reproduzíveis

    # Gera features aleatórias dentro de ranges realistas
    data = {
        'age': np.random.randint(18, 55, n_samples),
        'salary': np.random.uniform(1500, 15000, n_samples),
        'commute_time': np.random.randint(0, 181, n_samples),
        'gym_usage': np.random.randint(0, 31, n_samples),
        'meal_voucher': np.random.uniform(0, 1501, n_samples),
        'health_plan_tier': np.random.randint(1, 4, n_samples)
    }

    df = pd.DataFrame(data)

    # Cria target baseado em lógica de negócio
    # Satisfação aumenta com: salário alto, pouco commute, uso de benefícios

    df['satisfaction_score'] = (
        # Salário contribui 0-30 pontos
        (df['salary']/1500) * 30 +

        # Commute baixo contribui 0-20 pontos
        (1 - df['commute_time']/180) * 20 +

        # Uso de academia 0-15 pontos
        (df['gym_usage']/30) * 15 +

        # Vale-refeição 0-15 pontos
        (df['meal_voucher']/1500) * 15 +

        # Plano de saúde 0-20 pontos
        (df['health_plan_tier']/3) *20
    )

    # Adiciona ruído realista (vida não é 100% previsível)
    noise = np.random.normal(0, 5, n_samples)
    df['satisfaction_score'] = df['satisfaction_score'] + noise

    # Garante range 0-100
    df['satisfaction_score'] = df['satisfaction_score'].clip(0, 100)

    return df

def train_model():
    """
    Treina o modelo Random Forest e salva em disco
    """
    print("🔄 Gerando dados de treinamento...")
    df = generate_synthetic_data(n_samples=2000)

    print(f"✅ {len(df)} exemplos gerados")
    print(f"📊 Estatísticas do dataset:")
    print(df.describe())

    # Separa features (X) e target (y)
    X = df.drop('satisfaction_score', axis=1)
    y = df['satisfaction_score']

    # Divide em treino (80%) e teste (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\n📚 Treino: {len(X_train)} exemplos")
    print(f"🧪 Teste: {len(X_test)} exemplos")

    # Treina Random Forest
    print("\n🌲 Treinando Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=1
    )
    model.fit(X_train, y_train)

    # Avalia performance
    print("\n📈 Avaliando modelo...")
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n✨ RESULTADOS:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE:  {mae:.2f}")
    print(f"R² Score: {r2:.4f}")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n🎯 Importância das Features:")
    for idx, row in feature_importance.iterrows():
        print(f"  {row['feature']:20s}: {row['importance']:.4f}")
    
    # Salva modelo
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model, model_path)
    print(f"\n💾 Modelo salvo em: {model_path}")

    # Salva amostra dos dados
    sample_data_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    df.head(100).to_csv(sample_data_path, index=False)

    print(f"📄 Dados de exemplo salvos em: {sample_data_path}")

    print("\n🎉 Treinamento concluído com sucesso!")

    return model

if __name__ == '__main__':
    train_model()