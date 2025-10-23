#!/usr/bin/env bash

# Instalar as dependências
# echo "Instalando dependências..."
# pip install -r requirements.txt

# Executar as migrações do banco de dados
echo "Executando migrações..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py criar_funcoes_locais
python3 manage.py importar_dados_sql

echo "Build concluído com sucesso."
