import os



# # Para instalarmos a base de dados gerada
os.system("python manage.py loaddata database/db_import.json")
