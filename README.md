# 🎯 Benefit Predictor

> Aplicação Full-Stack de Machine Learning para prever satisfação de funcionários com benefícios corporativos

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Sobre o Projeto

**Benefit Predictor** é uma aplicação inteligente que utiliza Machine Learning para prever o nível de satisfação de funcionários baseado em:
- Dados demográficos (idade, salário)
- Tempo de deslocamento
- Uso de benefícios (academia, vale-refeição, plano de saúde)

O sistema fornece não apenas uma pontuação de satisfação (0-100), mas também **recomendações acionáveis** para o time de RH melhorar o engajamento.

### 🎯 Desenvolvido para

Este projeto foi criado como parte do processo seletivo para a posição de **Full Stack Developer** na [Yupii](https://yupii.pt), demonstrando habilidades em:
- ✅ Django + Django REST Framework
- ✅ PostgreSQL
- ✅ Machine Learning (scikit-learn)
- ✅ React (em desenvolvimento)
- ✅ Docker
- ✅ Desenvolvimento orientado a testes

---

## 🚀 Status do Projeto
```
Backend:   ████████████████  100% ✅ COMPLETO
Frontend:  ████████████████  100% ✅ COMPLETO
Docker:    ░░░░░░░░░░░░░░░░    0% 📋 PLANEJADO
```

### ✅ Funcionalidades Implementadas

**Backend (100%)**
- [x] API REST com Django REST Framework
- [x] Banco de dados PostgreSQL configurado
- [x] Modelo de Machine Learning treinado (Random Forest, R² = 0.92)
- [x] 4 endpoints principais funcionando
- [x] Sistema de validação de dados robusto
- [x] 17 testes unitários (100% passing)
- [x] Admin interface Django
- [x] Sistema de confidence scoring
- [x] Geração de recomendações acionáveis

**Frontend (100%)**
- [x] Formulário de predição com envio à API
- [x] Componente `ResultDisplay` com animação dinâmica e cores baseadas no score
- [x] Dashboard `Stats` com **Recharts** (média e número de predições)
- [x] Layout responsivo, estilizado com **TailwindCSS** e **Framer Motion**

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.0.2
- **API:** Django REST Framework 3.14.0
- **Database:** PostgreSQL 16
- **ML:** scikit-learn 1.4.0, pandas, numpy
- **Testing:** pytest, pytest-django
- **CORS:** django-cors-headers

### Frontend
- **Framework:** React 18 (planejado)
- **Build Tool:** Create React App
- **HTTP Client:** Axios
- **Estilização:** TailwindCSS 4.1
- **Charts:** Recharts 2.13
- **Animações:** Framer Motion 11.3

### DevOps
- **Containerization:** Docker, Docker Compose (planejado)
- **Version Control:** Git + GitHub

---

## 📊 Arquitetura
```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   React     │ HTTP │    Django    │      │ PostgreSQL │
│  Frontend   │─────▶│   REST API   │─────▶│  Database  │
│  (Port 5173)│      │  (Port 8000) │      │ (Port 5432)│
└─────────────┘      └──────────────┘      └────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  ML Model   │
                     │  (Random    │
                     │   Forest)   │
                     └─────────────┘
```

---

## 🎯 Machine Learning

### Modelo
- **Algoritmo:** Random Forest Regressor
- **Features:** 6 variáveis (age, salary, commute_time, gym_usage, meal_voucher, health_plan_tier)
- **Target:** Satisfaction score (0-100)
- **Performance:**
  - RMSE: 4.85
  - MAE: 3.62
  - R² Score: 0.9234

### Por que Random Forest?
1. **Robustez:** Lida bem com features de diferentes escalas
2. **Interpretabilidade:** Feature importance facilmente extraível
3. **Generalização:** Ensemble methods reduzem overfitting
4. **Performance:** Excelente para este caso de uso

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- PostgreSQL 16+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/soares-ari/benefit-predictor-ml.git
cd benefit-predictor-ml
```

### 2. Configure o Backend
```bash
cd backend

# Crie virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure PostgreSQL
# Crie o banco: createdb benefit_db

# Configure variáveis de ambiente (opcional)
# Edite backend/benefit_ai/settings.py com suas credenciais PostgreSQL

# Execute migrations
python manage.py migrate

# Treine o modelo ML
python api/ml/train_model.py

# Crie superuser (opcional)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

### 3. Teste a API

**Health Check:**
```bash
curl http://localhost:8000/api/health/
```

**Fazer uma Predição:**
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "salary": 5000,
    "commute_time": 45,
    "gym_usage": 12,
    "meal_voucher": 800,
    "health_plan_tier": 2
  }'
```

**Resposta Esperada:**
```json
{
  "satisfaction_score": 78.5,
  "confidence_level": "high",
  "recommendation": "Boa satisfação. Monitorar para manter o nível.",
  "prediction_id": 1
}
```

---

## 📚 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/health/` | Health check |
| `POST` | `/api/predict/` | Fazer predição |
| `GET` | `/api/predictions/` | Listar predições |
| `GET` | `/api/predictions/{id}/` | Detalhes de predição |
| `GET` | `/api/predictions/stats/` | Estatísticas gerais |

**Documentação completa da API:** [Em desenvolvimento]

---

## 🧪 Testes

### Executar Testes
```bash
cd backend
pytest -v
```

### Cobertura Atual
- **Total de Testes:** 17
- **Success Rate:** 100%
- **Cobertura:**
  - ✅ Health check endpoint
  - ✅ Predict endpoint (casos válidos e inválidos)
  - ✅ ViewSets (CRUD operations)
  - ✅ Models e validações
  - ✅ Edge cases

---

## 📁 Estrutura do Projeto
```
benefit-predictor-ml/
├── backend/                    # Django backend
│   ├── api/                   # API app
│   │   ├── ml/               # Machine Learning
│   │   │   ├── train_model.py
│   │   │   ├── predict.py
│   │   │   └── model.pkl
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tests.py
│   │   └── admin.py
│   ├── benefit_ai/           # Django settings
│   ├── manage.py
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/                  # React frontend (em desenvolvimento)
├── docs/                      # Documentação
├── README.md
└── .gitignore
```

---

## 🎓 Decisões Técnicas

### Por que Django e não FastAPI?
- **Requisito da vaga:** Stack da Yupii é Django
- **Admin panel:** Útil para RH visualizar predições
- **ORM robusto:** Django ORM é superior para relações complexas
- **Ecossistema maduro:** Mais packages e melhor documentação

### Por que PostgreSQL?
- **Requisito da vaga**
- **Confiabilidade:** ACID compliant
- **Features avançadas:** JSON fields, full-text search
- **Integração perfeita** com Django ORM

### Por que Random Forest?
- **Simplicidade:** Não requer normalização complexa
- **Interpretabilidade:** Feature importance clara
- **Performance:** R² de 0.92 é excelente para MVP
- **Produção-ready:** Rápido para inferência

---

## 🔮 Roadmap

### Fase 1: Backend (✅ Completo)
- [x] Django + DRF setup
- [x] PostgreSQL integration
- [x] ML model training
- [x] API endpoints
- [x] Unit tests

### Fase 2: Frontend (✅ Completo)
- [x] React setup com CRA
- [x] Formulário de entrada
- [x] Visualização de resultados
- [x] Dashboard de estatísticas
- [x] Integração com API

### Fase 3: DevOps (📋 Próximo)
- [ ] Docker Compose
- [ ] CI/CD com GitHub Actions
- [ ] Deploy em AWS/Heroku

### Fase 4: Melhorias (🔮 Futuro)
- [ ] Autenticação JWT
- [ ] Websockets para atualizações real-time
- [ ] Modelo mais sofisticado (XGBoost, Neural Networks)
- [ ] A/B testing de modelos
- [ ] Monitoramento de data drift

---

## 👨‍💻 Autor

**Ariel Soares**
- LinkedIn: [linkedin.com/in/ari-soares](https://www.linkedin.com/in/ari-soares)
- GitHub: [github.com/soares-ari](https://github.com/soares-ari)
- Email: ariel.b.p.soares@gmail.com

---

## 📝 Licença

Este projeto foi desenvolvido para fins de demonstração técnica no processo seletivo da Yupii.

---

## 🙏 Agradecimentos

- **Yupii** pela oportunidade de demonstrar minhas habilidades
- **Comunidade Django** pela excelente documentação
- **Comunidade scikit-learn** pelas ferramentas de ML

---

<p align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/soares-ari">Ariel Soares</a>
</p>

<p align="center">
  <sub>Projeto criado para o processo seletivo da Yupii - Novembro 2024</sub>
</p>
