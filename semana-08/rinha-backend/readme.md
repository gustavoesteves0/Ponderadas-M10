# Rinha Backend - FastAPI + PostgreSQL + Redis

Este projeto implementa uma API backend usando FastAPI com balanceamento de carga via Nginx, banco de dados PostgreSQL e cache Redis. A aplicação é totalmente containerizada usando Docker Compose.

## 🏗️ Estrutura do Projeto

```
rinha-backend/
├── backend/
│   ├── database/         # Configurações do banco de dados
│   ├── models/          # Modelos de dados SQLAlchemy
│   ├── routers/         # Rotas da API (user, transaction)
│   ├── schemas/         # Schemas Pydantic para validação
│   ├── services/        # Lógica de negócio
│   ├── Dockerfile       # Container da aplicação FastAPI
│   ├── main.py          # Arquivo principal da aplicação
│   └── requirements.txt # Dependências Python
├── nginx/
│   └── nginx.conf       # Configuração do load balancer
├── logs/                # Logs do Nginx
├── advanced_tests.py    # Testes avançados
├── test_suite.py        # Suite de testes
└── docker-compose.yml   # Orquestração dos containers
```

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para Python
- **PostgreSQL**: Banco de dados relacional
- **Redis**: Cache em memória
- **Nginx**: Load balancer e proxy reverso
- **Docker & Docker Compose**: Containerização e orquestração
- **SQLAlchemy**: ORM para Python
- **Asyncpg**: Driver assíncrono para PostgreSQL

## 📋 Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)

## 🔧 Como Executar

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd rinha-backend
```

### 2. Execute com Docker Compose
```bash
# Subir todos os serviços
docker-compose up -d

# Verificar se os containers estão rodando
docker-compose ps
```

### 3. Verificar se a aplicação está funcionando
```bash
# Testar o endpoint principal
curl http://localhost/

# Testar o ping (mostra qual instância respondeu)
curl http://localhost/ping
```

## 🏛️ Arquitetura

A aplicação utiliza uma arquitetura de microserviços com os seguintes componentes:

### Load Balancer (Nginx)
- **Porta**: 80
- Distribui requisições entre duas instâncias FastAPI
- Configuração de upstream com balanceamento round-robin

### Aplicações FastAPI (2 instâncias)
- **fastapi1**: Porta interna 8000 (mapeada para 8001 para debug)
- **fastapi2**: Porta interna 8000 (mapeada para 8002 para debug)
- Cada instância se conecta ao mesmo banco PostgreSQL e Redis

### Banco de Dados
- **PostgreSQL 15**: Porta 5432
- Database: `rinha`
- Usuário: `postgres`
- Senha: `postgres`

### Cache
- **Redis 7**: Porta 6379

## 🧪 Como Testar

### Testes Automatizados
```bash
# Executar suite de testes básicos
python test_suite.py

# Executar testes avançados
python advanced_tests.py
```

### Testes Manuais

#### 1. Testar Load Balancing
```bash
# Execute várias vezes para ver diferentes instâncias respondendo
curl http://localhost/ping
```

#### 2. Testar Endpoints da API
```bash
# Listar usuários
curl http://localhost/users

# Listar transações
curl http://localhost/transactions

# Criar usuário (exemplo)
curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -d '{"nome": "João", "email": "joao@email.com"}'
```

#### 3. Verificar Logs
```bash
# Logs do Nginx
docker-compose logs nginx

# Logs das aplicações FastAPI
docker-compose logs fastapi1
docker-compose logs fastapi2

# Logs do banco de dados
docker-compose logs db
```

## 🔍 Monitoramento e Debug

### Acessar containers individualmente
```bash
# Acessar instância 1 diretamente (debug)
curl http://localhost:8001/ping

# Acessar instância 2 diretamente (debug)
curl http://localhost:8002/ping
```

### Verificar status dos serviços
```bash
# Status de todos os containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f
```

### Conectar ao banco de dados
```bash
# Usando docker exec
docker exec -it db psql -U postgres -d rinha

# Ou usando cliente externo
psql -h localhost -p 5432 -U postgres -d rinha
```

## 🛑 Como Parar

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (apaga dados do banco)
docker-compose down -v

# Parar e remover imagens também
docker-compose down --rmi all
```

## 🐛 Solução de Problemas

### Problema: Containers não sobem
```bash
# Verificar logs
docker-compose logs

# Reconstruir containers
docker-compose up --build
```

### Problema: Erro de conexão com banco
```bash
# Verificar se o PostgreSQL está rodando
docker-compose logs db

# Verificar variáveis de ambiente
docker-compose config
```

### Problema: Load balancer não funciona
```bash
# Verificar configuração do Nginx
docker exec nginx nginx -t

# Recarregar configuração
docker exec nginx nginx -s reload
```

## 📝 Variáveis de Ambiente

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `DATABASE_URL` | URL de conexão com PostgreSQL | `postgresql+asyncpg://postgres:postgres@db:5432/rinha` |
| `INSTANCE_NAME` | Nome da instância FastAPI | `fastapi1` ou `fastapi2` |
| `POSTGRES_USER` | Usuário do PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL | `postgres` |
| `POSTGRES_DB` | Nome do banco de dados | `rinha` |