#!/usr/bin/env bash

# Instalar as dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Executar as migrações do banco de dados
echo "Executando migrações..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py criar_funcoes_locais
python manage.py importar_dados_sql

echo "Build concluído com sucesso."
