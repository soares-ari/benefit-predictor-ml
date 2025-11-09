# 🎓 Decisões Técnicas - Benefit Predictor

> Documentação detalhada das escolhas arquiteturais, trade-offs e desafios superados durante o desenvolvimento

**Autor:** Ariel Soares  
**Data:** Novembro 2024  
**Contexto:** Projeto técnico para processo seletivo Yupii (Full Stack Developer)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Stack Técnica](#stack-técnica)
3. [Decisões de Arquitetura](#decisões-de-arquitetura)
4. [Desafios Técnicos](#desafios-técnicos)
5. [Machine Learning](#machine-learning)
6. [Trade-offs e Limitações](#trade-offs-e-limitações)
7. [Aprendizados](#aprendizados)
8. [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral

### Contexto do Projeto

**Objetivo:** Criar uma aplicação full-stack que demonstre competências em:
- Backend (Django + DRF)
- Frontend (React)
- Machine Learning (scikit-learn)
- DevOps (Docker)
- Desenvolvimento orientado a testes

**Prazo:** 5 dias intensivos (06/11 - 11/11/2024)  
**Resultado:** MVP funcional com backend, frontend, ML e containerização

### Princípios Norteadores

1. **Pragmatismo sobre perfeição** - Entregar funcional > tecnicamente perfeito
2. **Commits progressivos** - Documentar evolução, não apenas resultado final
3. **Código defensável** - Poder explicar cada decisão na entrevista
4. **Qualidade mensurável** - Testes automatizados, métricas de ML

---

## 🛠️ Stack Técnica

### Backend: Django + Django REST Framework

**Decisão:** Django 5.0.2 com Django REST Framework 3.14.0

**Alternativas Consideradas:**
- FastAPI (Python moderno, async, rápido)
- Flask (minimalista, flexível)
- Express.js (Node.js, JavaScript full-stack)

**Justificativa:**

| Critério | Django | FastAPI | Flask |
|----------|--------|---------|-------|
| **Requisito da vaga** | ✅ Stack da Yupii | ❌ | ❌ |
| **Admin panel** | ✅ Out-of-the-box | ❌ Não tem | ⚠️ Manual |
| **ORM** | ✅ Robusto | ⚠️ SQLAlchemy | ⚠️ SQLAlchemy |
| **Segurança** | ✅ CSRF, XSS, SQL Injection | ⚠️ Manual | ⚠️ Manual |
| **Documentação** | ✅ Excelente | ✅ Boa | ⚠️ Fragmentada |
| **Tempo de setup** | ⚠️ ~1h | ✅ ~30min | ✅ ~20min |

**Conclusão:** Django foi escolhido principalmente por:
1. **Requisito explícito da vaga** (stack da Yupii)
2. **Admin interface** - Útil para RH visualizar predições sem frontend
3. **Segurança built-in** - Produção-ready desde o início
4. **Ecossistema maduro** - Mais packages, melhor suporte

**Trade-off aceito:** Setup inicial mais lento que FastAPI, mas compensado pela robustez.

---

### Frontend: React + Create React App

**Decisão:** React 18.3 com Create React App

**Alternativas Consideradas:**
- Vite (tentado, falhou - ver [Desafios Técnicos](#desafio-1-vite--windows))
- Next.js (framework React com SSR)
- Vue.js (alternativa ao React)

**Justificativa:**

**Por que React:**
- Experiência prévia (2 anos)
- Comunidade massive
- Mercado demanda
- Component-based architecture
- Hooks modernos

**Por que CRA e não Vite:**

**Cronologia:**
1. **Tentativa inicial:** Vite (ferramenta moderna, build rápido)
2. **Problema:** Conflitos com `esbuild.exe` no Windows
   - Erro: `EBUSY: resource busy or locked`
   - Causa: Windows Defender bloqueando binários
3. **Tentativas de resolução:**
   - Reinstalação Node.js (3x)
   - Variáveis de ambiente PATH
   - Yarn, pnpm (alternativas ao npm)
   - `--ignore-scripts` flag
4. **Decisão pragmática:** Migrar para CRA após ~2h troubleshooting
5. **Resultado:** CRA funcionou imediatamente

**Lição:** Em contexto de prazo apertado, usar ferramenta estável > insistir na "ideal".

**Justificativa para entrevista:**
> "Vite seria mais rápido, mas apresentou problemas específicos do Windows. Em uma startup com deadline, priorizei entregar funcional. Em produção, usaria Vite em ambiente Linux ou resolveria configurações Windows adequadamente."

---

### Styling: TailwindCSS 4.0

**Decisão:** Tailwind CSS 4.0

**Alternativas:**
- Material-UI (component library completa)
- CSS Modules (CSS tradicional modularizado)
- Styled Components (CSS-in-JS)

**Justificativa:**

| Critério | Tailwind | Material-UI | CSS Modules |
|----------|----------|-------------|-------------|
| **Velocidade** | ✅ Muito rápida | ⚠️ Média | ❌ Lenta |
| **Bundle size** | ✅ Pequeno | ❌ Grande | ✅ Pequeno |
| **Customização** | ✅ Total | ⚠️ Limitada | ✅ Total |
| **Consistência** | ✅ Design system | ✅ Design system | ❌ Manual |
| **Responsividade** | ✅ Trivial | ✅ Boa | ⚠️ Manual |

**Conclusão:** Tailwind foi escolhido por:
1. **Velocidade de desenvolvimento** - 3x mais rápido que CSS puro
2. **Design system consistente** - Spacing, colors, typography predefinidos
3. **Bundle otimizado** - Purge automático de CSS não usado
4. **Responsividade fácil** - Breakpoints como `sm:`, `md:`, `lg:`
5. **Sem overhead de componentes** - Ao contrário de MUI

**Exemplo prático:**
```jsx
// Tailwind (1 linha)
<button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">

// CSS Modules (arquivo separado, múltiplas linhas)
<button className={styles.button}>
// styles.module.css:
// .button { background: #2563eb; padding: 0.75rem 1.5rem; ... }
```

---

### Database: PostgreSQL 16

**Decisão:** PostgreSQL 16-alpine

**Alternativas:**
- MySQL (popular, compatível)
- SQLite (desenvolvimento rápido)
- MongoDB (NoSQL, flexível)

**Justificativa:**

**PostgreSQL escolhido por:**
1. **Requisito da vaga**
2. **ACID compliance** - Transações confiáveis
3. **Features avançadas:**
   - JSON fields (para logs, metadata)
   - Full-text search
   - Array types
   - Window functions
4. **Performance excelente** para datasets médios
5. **Integração perfeita** com Django ORM

**Trade-off:** Setup inicial mais complexo que SQLite, mas necessário para produção.

---

### Containerização: Docker + Docker Compose

**Decisão:** Docker Compose com 3 serviços

**Alternativas:**
- Kubernetes (overkill para MVP)
- Heroku Buildpacks (vendor lock-in)
- VMs tradicionais (pesadas, lentas)

**Justificativa:**

**Docker Compose escolhido por:**
1. **Ambiente consistente** - "Works on my machine" resolvido
2. **Onboarding rápido** - Novo dev: `docker-compose up`
3. **Isolamento de serviços** - DB, backend, frontend separados
4. **Produção-similar** - Arquitetura escalável
5. **Demonstração de competência DevOps**

**Arquitetura:**
```yaml
services:
  db:        PostgreSQL 16-alpine (lightweight)
  backend:   Django + Python 3.11-slim
  frontend:  React + Node 20-alpine
```

**Desafios superados:** Ver [Desafio #3: Docker I/O Errors](#desafio-3-docker-io-errors)

---

## 🏗️ Decisões de Arquitetura

### API Design: RESTful

**Decisão:** REST API com Django REST Framework

**Alternativas:**
- GraphQL (flexibilidade de queries)
- gRPC (performance, type-safe)
- WebSockets (real-time)

**Justificativa REST:**
1. **Simplicidade** - Padrão bem estabelecido
2. **Cacheable** - HTTP caching natural
3. **Stateless** - Escalabilidade horizontal fácil
4. **Tooling** - Postman, curl, browsers suportam
5. **DRF integration** - Serializers, ViewSets, routers automáticos

**Endpoints desenhados:**
```
GET  /api/health/              -> Health check
POST /api/predict/             -> Nova predição
GET  /api/predictions/         -> Lista paginada
GET  /api/predictions/{id}/    -> Detalhes
GET  /api/predictions/stats/   -> Agregações
```

**Padrão seguido:** Richardson Maturity Model - Level 2 (HTTP verbs + status codes)

---

### Frontend Architecture: Component-Based

**Decisão:** Componentes funcionais com Hooks

**Estrutura:**
```
src/
├── components/
│   ├── PredictionForm.jsx    -> Formulário (estado local)
│   ├── ResultDisplay.jsx     -> Exibição (props)
│   ├── Stats.jsx              -> Dashboard (fetch + state)
│   └── Footer.jsx             -> Stateless
├── services/
│   └── api.js                 -> Axios config centralizado
└── App.jsx                    -> Orquestração
```

**Princípios aplicados:**
1. **Single Responsibility** - Cada componente uma função
2. **Composition over Inheritance** - Componentes compostos
3. **Controlled Components** - Estado explícito
4. **Separation of Concerns** - Lógica de API separada

---

### State Management: Local State

**Decisão:** `useState` local, sem Redux/Context

**Justificativa:**
- Aplicação pequena (~4 componentes)
- Sem estado global complexo
- Comunicação pai-filho simples
- Redux seria **over-engineering**

**Quando usar Redux/Context:**
- Aplicação com >10 componentes
- Estado compartilhado entre muitos níveis
- Necessidade de middleware (logging, persistence)

---

## 🤖 Machine Learning

### Algoritmo: Random Forest Regressor

**Decisão:** Random Forest com 100 estimators

**Alternativas Consideradas:**

| Modelo | R² Esperado | Interpretabilidade | Velocidade | Complexidade |
|--------|-------------|-------------------|------------|--------------|
| **Linear Regression** | 0.70-0.75 | ✅ Alta | ✅ Rápida | ✅ Simples |
| **Random Forest** | 0.85-0.90 | ✅ Alta | ✅ Rápida | ⚠️ Média |
| **XGBoost** | 0.90-0.95 | ⚠️ Média | ⚠️ Média | ❌ Alta |
| **Neural Network** | 0.85-0.95 | ❌ Baixa | ❌ Lenta | ❌ Muito alta |

**Justificativa Random Forest:**

1. **Performance excelente:**
   - R² CV: 0.8684 (± 0.03)
   - R² Test: 0.8677
   - Gap: 9% (aceitável)

2. **Interpretabilidade:**
```
   Feature Importance:
   salary: 73.84%  <- Principal driver (esperado!)
   commute_time: 7.13%
   health_plan: 6.88%
```
   Insights acionáveis para RH!

3. **Robustez:**
   - Não requer normalização/scaling
   - Lida bem com outliers
   - Ensemble reduz overfitting

4. **Velocidade:**
   - Treinamento: ~2s (2000 samples)
   - Inferência: <10ms
   - Produção-ready

5. **Manutenibilidade:**
   - Código simples
   - Fácil de re-treinar
   - Sem dependencies pesadas (TensorFlow, etc)

**Trade-off:** XGBoost teria R² ~2-3% maior, mas:
- Setup mais complexo
- Tuning de hiperparâmetros demorado
- Menor interpretabilidade
- Não justifica para MVP

---

### Validação do Modelo

**Abordagem:**
1. **Cross-Validation 5-fold** - Medir generalização
2. **Hold-out Test (80/20)** - Detectar overfitting
3. **Regularização** - max_depth=8, min_samples_split=10

**Resultados:**

**Antes da regularização:**
- R² Train: 0.9854
- R² Test: 0.8848
- **Gap: 10.06%** ⚠️ Overfitting moderado

**Depois da regularização:**
- R² Train: 0.9580
- R² Test: 0.8677
- **Gap: 9.03%** ✅ Aceitável

**Interpretação:** Gap de 9% é normal para:
- Dataset sintético
- Modelo ensemble (Random Forest)
- MVP (não produção crítica)

**Para produção:**
- Coletar dados reais
- Expandir dataset (>5000 samples)
- A/B testing entre modelos
- Monitorar data drift

---

### Feature Engineering

**Features selecionadas:**

| Feature | Tipo | Range | Justificativa |
|---------|------|-------|---------------|
| age | int | 18-100 | Proxy para senioridade |
| salary | float | 1320+ | **Principal driver** |
| commute_time | int | 0-300 min | Qualidade de vida |
| gym_usage | int | 0-30 dias | Engajamento com benefícios |
| meal_voucher | float | 0+ | Benefício monetário |
| health_plan_tier | int | 1-3 | Qualidade do plano |

**Features NÃO incluídas (por quê):**
- ❌ Nome, CPF → Não preditivas, LGPD concerns
- ❌ Departamento → Aumentaria dimensionalidade sem ganho
- ❌ Tempo de empresa → Não disponível facilmente

**Feature Importance validou escolhas:**
- Salary dominante (74%) - esperado!
- Outros features contribuem ~26% - relevantes mas secundários

---

## 🔥 Desafios Técnicos

### Desafio #1: Vite + Windows

**Problema:**
```
Error: EBUSY: resource busy or locked, rmdir 'node_modules\esbuild'
Error: EPERM: operation not permitted
```

**Causa Raiz:**
- Windows Defender bloqueando `esbuild.exe`
- PowerShell não reconhecendo comandos Node
- Conflitos entre npm/yarn/pnpm

**Tentativas de Resolução (2h):**
1. ✅ Reinstalação Node.js (3x)
2. ✅ Correção variáveis ambiente PATH
3. ✅ Tentativa com Yarn
4. ✅ Tentativa com pnpm
5. ✅ `npm install --ignore-scripts`
6. ❌ Nenhuma resolveu completamente

**Decisão:** Migrar para Create React App

**Aprendizado:**
- Time-boxing importante (2h max por problema)
- Pragmatismo > purismo técnico
- CRA é "boring technology" - funciona!

**Para entrevista:**
> "Após 2h troubleshooting Vite no Windows, migrei pragmaticamente para CRA. Demonstra saber quando mudar de abordagem ao invés de insistir em solução problemática. Em produção, usaria Vite em Linux ou resolveria configurações Windows adequadamente."

---

### Desafio #2: Overfitting do Modelo ML

**Problema:**
```
R² Train: 0.9854
R² Test:  0.8848
Gap:      10.06% <- Overfitting!
```

**Diagnóstico:**
1. Dataset inicial: apenas 100 amostras (insuficiente!)
2. Random Forest com `max_depth=10` (muito profundo)
3. `min_samples_split=2` (sem regularização)

**Solução Implementada:**

**Passo 1: Aumentar dataset**
```python
# Antes: 100 amostras
df = generate_synthetic_data(n_samples=100)

# Depois: 2000 amostras
df = generate_synthetic_data(n_samples=2000)
```

**Resultado:** R² CV subiu de 0.67 para 0.88 ✅

**Passo 2: Regularização**
```python
# Antes
RandomForestRegressor(max_depth=10, min_samples_split=2)

# Depois
RandomForestRegressor(max_depth=8, min_samples_split=10)
```

**Resultado:** Gap reduziu de 10% para 9% ✅

**Aprendizado:**
- Validação rigorosa essencial
- Dataset size importa muito
- Regularização >> Complexidade

---

### Desafio #3: Docker I/O Errors

**Problema:**
```
ERROR: Could not install packages due to an OSError: [Errno 5] Input/output error
FATAL: could not open file "global/pg_filenode.map": I/O error
```

**Causa:** Docker Desktop no Windows sob stress (disco cheio, volumes corrompidos)

**Cronologia (3h):**
1. **Tentativa 1:** Build inicial → I/O error no pip install
2. **Ação:** Liberado 15GB espaço em disco
3. **Tentativa 2:** Build ok, mas DB com I/O error
4. **Ação:** `docker system prune -a --volumes` (limpeza total)
5. **Tentativa 3:** Network DNS não resolvendo hostname "db"
6. **Ação:** Aumentado sleep de 10s → 25s no entrypoint
7. **Tentativa 4:** ✅ **FUNCIONOU!**

**Soluções Aplicadas:**

**1. Entrypoint script robusto:**
```bash
#!/bin/bash
echo "⏳ Waiting 25 seconds for network and PostgreSQL..."
sleep 25  # Aguarda DNS resolver + DB iniciar

python manage.py migrate --noinput || {
    echo "❌ Migration failed, retrying in 10s..."
    sleep 10
    python manage.py migrate --noinput
}
```

**2. Docker Compose sem condition:**
```yaml
backend:
  depends_on:
    - db  # SEM condition: service_healthy
```
**Motivo:** Healthcheck falhando no Windows

**3. Volumes limpos:**
```bash
docker-compose down -v  # Remove volumes corrompidos
```

**Aprendizado:**
- Docker no Windows tem limitações
- Sleep pragmático > healthcheck complexo
- Retry logic essencial
- Limpar cache/volumes resolve 80% dos problemas

---

### Desafio #4: CORS + Frontend-Backend Integration

**Problema:** Frontend não conseguia fazer requests para backend
```javascript
// Erro no console
Access to XMLHttpRequest at 'http://localhost:8000/api/predict/'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Causa:** CORS não configurado no Django

**Solução:**

**1. Instalar django-cors-headers:**
```bash
pip install django-cors-headers
```

**2. Configurar settings.py:**
```python
INSTALLED_APPS = [
    'corsheaders',  # Adicionar
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # No topo!
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React (CRA)
    "http://localhost:5173",  # React (Vite)
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
```

**Aprendizado:**
- CORS é "feature", não bug
- Configurar corretamente desde o início
- Ambiente dev != produção (origins diferentes)

---

## ⚖️ Trade-offs e Limitações

### Limitações Técnicas

**1. Dataset Sintético**

❌ **Limitação:**
- Dados não são reais
- Padrões artificiais
- Não captura complexidade real

✅ **Mitigação:**
- Distribuições realistas
- Validação rigorosa (CV + hold-out)
- Documentado claramente

**Para produção:**
- Coletar dados reais de RH
- Validar com A/B testing
- Retreinar periodicamente

---

**2. Sem Autenticação**

❌ **Limitação:**
- API aberta (qualquer um pode usar)
- Sem multi-tenancy
- Sem rate limiting

✅ **Justificativa MVP:**
- Não era requisito
- Tempo limitado (5 dias)
- Foco em ML + integração

**Para produção:**
- JWT authentication
- Role-based access (RH vs Admin)
- Rate limiting (Django Ratelimit)

---

**3. Testes Frontend Ausentes**

❌ **Limitação:**
- Sem React Testing Library
- Sem testes E2E
- Apenas testes manuais

✅ **Justificativa:**
- Backend tem 17 testes (100% passing)
- Tempo priorizou backend
- Frontend visualmente validado

**Para produção:**
- React Testing Library (unit)
- Cypress (E2E)
- Coverage >80%

---

**4. Deploy Manual (Não Automatizado)**

❌ **Limitação:**
- Sem CI/CD
- Deploy manual com Docker
- Sem blue-green deployment

✅ **Justificativa:**
- MVP local
- Docker Compose suficiente
- GitHub Actions seria next step

**Para produção:**
- GitHub Actions (CI/CD)
- Deploy em AWS ECS ou Heroku
- Monitoramento (Sentry, DataDog)

---

### Trade-offs Conscientes

**1. Random Forest vs XGBoost**

| Aspecto | Random Forest ✅ | XGBoost |
|---------|------------------|---------|
| R² Score | 0.87 | ~0.90 |
| Interpretability | Alta | Média |
| Setup | Simples | Complexo |
| Tuning | Rápido | Demorado |

**Decisão:** Random Forest suficiente para MVP. XGBoost seria premature optimization.

---

**2. REST vs GraphQL**

| Aspecto | REST ✅ | GraphQL |
|---------|---------|----------|
| Simplicidade | Alta | Média |
| Caching | HTTP nativo | Manual |
| Learning curve | Baixa | Alta |
| Over-fetching | Possível | Não |

**Decisão:** REST mais adequado para API simples com endpoints bem definidos.

---

**3. Local State vs Redux**

| Aspecto | Local State ✅ | Redux |
|---------|----------------|-------|
| Complexidade | Baixa | Alta |
| Boilerplate | Mínimo | Muito |
| Debug | console.log | DevTools |
| Necessário? | Não | Não |

**Decisão:** Redux seria over-engineering para 4 componentes simples.

---

## 📚 Aprendizados

### Técnicos

1. **Docker no Windows é desafiador**
   - WSL2 ajuda mas não resolve tudo
   - I/O errors são comuns sob stress
   - Healthchecks podem falhar (use sleep pragmático)

2. **Vite excelente mas não universal**
   - Windows pode ter problemas com esbuild
   - CRA é "boring" mas confiável
   - Nem sempre "latest and greatest" é melhor

3. **Validação ML é essencial**
   - Cross-validation >> single train/test split
   - Dataset size importa MUITO
   - Interpretabilidade > 1% extra de R²

4. **Time-boxing previne rabbit holes**
   - 2h max por problema não-crítico
   - Saber quando pivotar é habilidade
   - "Good enough" beats "perfect too late"

### Processo

1. **Commits progressivos são valiosos**
   - Documentam jornada
   - Facilitam debugging
   - Mostram pensamento iterativo

2. **Documentação durante > depois**
   - Escrever decisões enquanto frescas
   - README atualizado incrementalmente
   - TECHNICAL_DECISIONS captura contexto

3. **Testes dão confiança**
   - 17 testes backend permitem refactoring
   - TDD seria ideal mas não obrigatório
   - Coverage >80% é suficiente

### Soft Skills

1. **Pragmatismo é subestimado**
   - MVP funcional > tecnicamente perfeito
   - Entregar valor > usar tech da moda
   - Cliente não vê arquitetura, vê resultado

2. **Comunicação de trade-offs**
   - Decisões sempre têm custo
   - Explicar "por quês" é crucial
   - Honestidade técnica > blefe

---

## 🚀 Próximos Passos

### Se eu tivesse mais 2 semanas:

**Semana 1: Refinamentos**
- [ ] Adicionar autenticação JWT
- [ ] Implementar rate limiting
- [ ] Testes frontend com RTL
- [ ] CI/CD com GitHub Actions
- [ ] Deploy em Heroku/AWS

**Semana 2: Features Avançadas**
- [ ] Dashboard analytics avançado
- [ ] Exportar relatórios PDF
- [ ] Sistema de notificações
- [ ] A/B testing de modelos
- [ ] Monitoramento (Sentry, DataDog)

### Se fosse projeto real de produção:

**Arquitetura:**
- Microservices (ML service separado)
- Message queue (Celery para predições assíncronas)
- Redis para caching
- Load balancer (Nginx)

**ML:**
- Pipeline automático de retreinamento
- Feature store (ex: Feast)
- Monitoramento de data drift
- Ensemble de múltiplos modelos

**Frontend:**
- Next.js (SSR, SEO)
- TypeScript (type safety)
- Storybook (component library)
- E2E tests (Cypress)

**DevOps:**
- Kubernetes (orquestração)
- Terraform (IaC)
- Prometheus + Grafana (monitoring)
- Blue-green deployment

---

## 📊 Conclusão

### Métricas de Sucesso

✅ **Backend:** 100% funcional com 17 testes  
✅ **Frontend:** 100% integrado e responsivo  
✅ **ML:** R² 0.87, interpretável e validado  
✅ **Docker:** 3 serviços containerizados  
✅ **Documentação:** README + TECHNICAL_DECISIONS completos  
✅ **Prazo:** Entregue em 5 dias  

### Principais Conquistas

1. **Resolução de problemas** - Docker I/O, Vite Windows, ML overfitting
2. **Pragmatismo** - Pivotar de Vite → CRA salvou 1 dia
3. **Qualidade** - 17 testes, validação ML rigorosa, documentação completa
4. **Entrega** - MVP funcional, demonstrável, pronto para apresentação

### O Que Faria Diferente

1. **Testar Docker MAIS CEDO** - Descobrir problemas I/O antes
2. **Começar com CRA** - Não tentar Vite no Windows
3. **Dataset real desde início** - Mesmo pequeno, melhor que sintético
4. **Testes frontend incrementais** - Não deixar para depois

---

## 🎤 Para a Entrevista

### Narrativa de 2 Minutos

> "Nos últimos 5 dias, desenvolvi um projeto full-stack do zero: backend Django com Random Forest (R² 0.87), frontend React integrado, tudo containerizado com Docker.
>
> Enfrentei desafios técnicos reais - Vite com problemas no Windows, Docker com I/O errors, modelo com overfitting. Cada vez, diagnostiquei, tentei soluções, e quando necessário, pivotei pragmaticamente.
>
> O projeto demonstra não só conhecimento técnico (Django, React, ML, Docker) mas também maturidade: saber fazer trade-offs, documentar decisões, e entregar valor dentro de prazo.
>
> Está pronto para demo: posso mostrar predição em tempo real, explicar decisões de arquitetura, e discutir próximos passos para produção."

### Perguntas Esperadas & Respostas

**P: "Por que CRA e não Vite?"**  
**R:** "Vite seria ideal, mas apresentou problemas específicos do Windows (esbuild bloqueado). Após 2h troubleshooting, migrei pragmaticamente para CRA. Demonstra saber quando mudar de abordagem."

**P: "Por que não testes no frontend?"**  
**R:** "Priorizei backend (17 testes) por ser mais crítico. Com mais tempo, adicionaria RTL. Trade-off consciente dentro do prazo."

**P: "Como escalaria isso?"**  
**R:** "Microservices para ML (Celery async), Redis caching, Kubernetes orquestração, monitoramento com Prometheus. Mas para MVP, arquitetura atual é apropriada."

**P: "Dataset sintético não é problema?"**  
**R:** "É limitação conhecida e documentada. Validação rigorosa (CV + hold-out) mitiga. Em produção, usaria dados reais e retreinamento periódico."

---

## 📞 Contato

**Ariel Soares**  
Machine Learning Engineer | Full Stack Developer

📧 ariel.b.p.soares@gmail.com  
💼 [linkedin.com/in/ari-soares](https://www.linkedin.com/in/ari-soares)  
🐙 [github.com/soares-ari](https://github.com/soares-ari)

---

<p align="center">
  <strong>Este documento captura o processo de pensamento, não apenas o resultado final.</strong>
</p>

<p align="center">
  <sub>Benefit Predictor - Novembro 2024</sub>
</p>