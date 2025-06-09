FROM python:3.11-slim

WORKDIR /app

# Copia o requirements.txt
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando para rodar sua aplicação (exemplo)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
