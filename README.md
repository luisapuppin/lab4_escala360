# Escala 360

## O que é?
Projeto de Desenvolvimento de Software feito para a disciplina de Laboratório de Inovação 4 cursada na Faculdade de Tecnologia e Inovação Senac DF no ano de 2025.

## Objetivo
Desenvolver um sistema de escala e plantões para clínicas ou hospitais implementando principalmente uma funcionalidade que organize a alocação de profissionais em plantões, considerando substituições, conflitos de horários, alertas e notificações automáticas.

## Linguagem e ferramentas
O projeto utiliza linguagem Python e o framework Django.

## Migração de dados
O projeto apresenta um banco de dados pré-configurado para visualização. Para realizar a migração do modelo de dados e popular os dados faça os seguintes comandos no terminal:

```bash
python manage.py makemigrations

python manage.py migrate

python manage.py criar_funcoes_locais

python manage.py importar_dados_sql
```

## Iniciar o servidor
Para iniciar o servidor do Django escreva o seguinte comando no terminal

```bash
python manage.py runserver
```
