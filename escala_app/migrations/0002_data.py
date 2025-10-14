# Arquivo gerado para carregar dados de forma programática sem dbshell

from django.db import migrations
import os
from django.conf import settings

def load_data_from_sql(apps, schema_editor):
    # O arquivo SQL que ajustamos com os INSERTs do Django (escala_app_...)
    sql_file_path = os.path.join(settings.BASE_DIR, 'escala_app', 'fixtures', 'escala360.sql')
    
    # Executa o conteúdo do arquivo SQL diretamente na conexão do banco
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_statements = file.read()
        with schema_editor.connection.cursor() as cursor:
            cursor.executescript(sql_statements)

class Migration(migrations.Migration):

    dependencies = [
        # Depende da sua primeira migração de criação de modelos (models)
        ('escala_app', '0001_initial'),
    ]

    operations = [
        # Cria uma operação que executa a função acima
        migrations.RunPython(load_data_from_sql),
    ]
