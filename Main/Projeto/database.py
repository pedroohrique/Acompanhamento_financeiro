import pyodbc
from logger import configura_log

def database_connection():
    server = 'DESKTOP-98I4FGO'
    database = 'FINANCEIRO'
    user = 'Admin'
    password = '66tUa3ue'

    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + user + ';PWD=' + password)
        cursor = connection.cursor()
        return connection, cursor

    except pyodbc.Error as e:
        log = configura_log("database.py")
        log.error(f"Falha ao conectar ao banco de dados local: {e}")
        return None

