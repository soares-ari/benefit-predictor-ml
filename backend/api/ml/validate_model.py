"""
Script de validação do modelo ML.
Verifica overfitting e performance de generalização.
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor


def load_model_and_data():
    """Carrega modelo e GERA dados de validação."""
    from train_model import generate_synthetic_data  # Import da função
    
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    model = joblib.load(model_path)
    
    # GERA 2000 amostras para validação (não usa sample_data.csv)
    print("   Gerando dataset de validação (2000 amostras)...")
    df = generate_synthetic_data(n_samples=2000)
    
    return model, df


def validate_with_cross_validation(model, X, y, cv=5):
    """
    Validação cruzada para detectar overfitting.
    
    Se R² CV for muito menor que R² treino → overfitting!
    """
    print("\n" + "="*60)
    print("🔄 VALIDAÇÃO CRUZADA (Cross-Validation)")
    print("="*60)
    
    # Diferentes métricas
    r2_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    neg_mse_scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error')
    neg_mae_scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
    
    # Converter negativos para positivos
    mse_scores = -neg_mse_scores
    mae_scores = -neg_mae_scores
    rmse_scores = np.sqrt(mse_scores)
    
    print(f"\n📊 Resultados ({cv}-fold CV):")
    print(f"   R² Score:  {r2_scores.mean():.4f} (± {r2_scores.std():.4f})")
    print(f"   RMSE:      {rmse_scores.mean():.2f} (± {rmse_scores.std():.2f})")
    print(f"   MAE:       {mae_scores.mean():.2f} (± {mae_scores.std():.2f})")
    
    print(f"\n📈 R² por fold:")
    for i, score in enumerate(r2_scores, 1):
        print(f"   Fold {i}: {score:.4f}")
    
    return {
        'r2_mean': r2_scores.mean(),
        'r2_std': r2_scores.std(),
        'rmse_mean': rmse_scores.mean(),
        'mae_mean': mae_scores.mean()
    }


def evaluate_on_holdout(model, X, y, test_size=0.2):
    """
    Avalia em conjunto de teste separado (hold-out).
    """
    print("\n" + "="*60)
    print("🧪 AVALIAÇÃO HOLD-OUT (Test Set)")
    print("="*60)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Predições
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Métricas treino
    r2_train = r2_score(y_train, y_train_pred)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
    mae_train = mean_absolute_error(y_train, y_train_pred)
    
    # Métricas teste
    r2_test = r2_score(y_test, y_test_pred)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
    mae_test = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\n📊 TREINO (80% dos dados):")
    print(f"   R² Score:  {r2_train:.4f}")
    print(f"   RMSE:      {rmse_train:.2f}")
    print(f"   MAE:       {mae_train:.2f}")
    
    print(f"\n📊 TESTE (20% dos dados):")
    print(f"   R² Score:  {r2_test:.4f}")
    print(f"   RMSE:      {rmse_test:.2f}")
    print(f"   MAE:       {mae_test:.2f}")
    
    # Diagnóstico de overfitting
    print(f"\n🔍 DIAGNÓSTICO:")
    diff = r2_train - r2_test
    print(f"   Diferença R² (treino - teste): {diff:.4f}")
    
    if diff > 0.10:
        print(f"   ⚠️  OVERFITTING DETECTADO!")
        print(f"   → Modelo memoriza treino mas não generaliza bem")
    elif diff > 0.05:
        print(f"   ⚡ Overfitting leve (aceitável para MVP)")
    else:
        print(f"   ✅ Boa generalização!")
    
    return {
        'r2_train': r2_train,
        'r2_test': r2_test,
        'overfitting_gap': diff
    }


def check_feature_importance(model, feature_names):
    """Mostra features mais importantes."""
    print("\n" + "="*60)
    print("🎯 IMPORTÂNCIA DAS FEATURES")
    print("="*60)
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n")
    for _, row in importance_df.iterrows():
        bar = '█' * int(row['importance'] * 50)
        print(f"   {row['feature']:20s} {bar} {row['importance']:.4f}")
    
    return importance_df


def suggest_improvements(cv_results, holdout_results):
    """Sugere melhorias baseado nos resultados."""
    print("\n" + "="*60)
    print("💡 SUGESTÕES DE MELHORIA")
    print("="*60)
    
    r2_cv = cv_results['r2_mean']
    overfitting_gap = holdout_results['overfitting_gap']
    
    suggestions = []
    
    # Verifica performance
    if r2_cv < 0.80:
        suggestions.append("⚠️  R² CV baixo - considere:")
        suggestions.append("   • Coletar mais dados")
        suggestions.append("   • Adicionar features relevantes")
        suggestions.append("   • Testar outros algoritmos (XGBoost)")
    elif r2_cv >= 0.85:
        suggestions.append("✅ R² CV excelente!")
    
    # Verifica overfitting
    if overfitting_gap > 0.10:
        suggestions.append("⚠️  Overfitting significativo - ajustar:")
        suggestions.append("   • Reduzir max_depth (ex: 8 ou 6)")
        suggestions.append("   • Aumentar min_samples_split (ex: 10)")
        suggestions.append("   • Reduzir n_estimators")
        suggestions.append("   • Adicionar mais dados de treino")
    elif overfitting_gap > 0.05:
        suggestions.append("⚡ Overfitting leve - monitorar mas aceitável")
    else:
        suggestions.append("✅ Sem overfitting detectado!")
    
    # Sugestões gerais
    suggestions.append("\n📋 Para produção, considere:")
    suggestions.append("   • Implementar monitoramento de data drift")
    suggestions.append("   • A/B testing com modelos alternativos")
    suggestions.append("   • Retreinamento periódico (ex: mensal)")
    suggestions.append("   • Validação com dados reais (não sintéticos)")
    
    for suggestion in suggestions:
        print(suggestion)


def retrain_if_needed(X, y, current_model):
    """
    Se overfitting for detectado, retreina com regularização.
    """
    print("\n" + "="*60)
    print("🔧 RETREINAMENTO COM REGULARIZAÇÃO")
    print("="*60)
    
    print("\nTreinando modelo regularizado...")
    print("   Parâmetros: max_depth=8, min_samples_split=10")
    
    regularized_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=8,           # Reduzido de 10
        min_samples_split=10,  # Aumentado de 2
        random_state=42,
        n_jobs=-1
    )
    
    # Treina
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    regularized_model.fit(X_train, y_train)
    
    # Avalia
    y_train_pred = regularized_model.predict(X_train)
    y_test_pred = regularized_model.predict(X_test)
    
    r2_train = r2_score(y_train, y_train_pred)
    r2_test = r2_score(y_test, y_test_pred)
    
    print(f"\n📊 Resultados do modelo regularizado:")
    print(f"   R² Treino: {r2_train:.4f}")
    print(f"   R² Teste:  {r2_test:.4f}")
    print(f"   Gap:       {r2_train - r2_test:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(regularized_model, X, y, cv=5, scoring='r2')
    print(f"   R² CV:     {cv_scores.mean():.4f} (± {cv_scores.std():.4f})")
    
    return regularized_model


def main():
    """Executa validação completa."""
    print("\n" + "="*60)
    print("🎯 VALIDAÇÃO DO MODELO - BENEFIT PREDICTOR")
    print("="*60)
    
    # 1. Carrega modelo e dados
    print("\n📂 Carregando modelo e dados...")
    model, df = load_model_and_data()
    
    X = df.drop('satisfaction_score', axis=1)
    y = df['satisfaction_score']
    feature_names = X.columns.tolist()
    
    print(f"   ✅ Modelo carregado: {type(model).__name__}")
    print(f"   ✅ Dados carregados: {len(df)} amostras, {len(feature_names)} features")
    
    # 2. Cross-validation
    cv_results = validate_with_cross_validation(model, X, y, cv=5)
    
    # 3. Hold-out test
    holdout_results = evaluate_on_holdout(model, X, y, test_size=0.2)
    
    # 4. Feature importance
    check_feature_importance(model, feature_names)
    
    # 5. Sugestões
    suggest_improvements(cv_results, holdout_results)
    
    # 6. Retreinamento se necessário
    if holdout_results['overfitting_gap'] > 0.10:
        print("\n⚠️  Overfitting detectado!")
        response = input("\n   Retreinar com regularização? (s/n): ")
        
        if response.lower() == 's':
            new_model = retrain_if_needed(X, y, model)
            
            save = input("\n   Salvar modelo regularizado? (s/n): ")
            if save.lower() == 's':
                model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
                joblib.dump(new_model, model_path)
                print(f"\n   ✅ Modelo salvo em: {model_path}")
    
    print("\n" + "="*60)
    print("✅ VALIDAÇÃO COMPLETA!")
    print("="*60)


if __name__ == '__main__':
    main()