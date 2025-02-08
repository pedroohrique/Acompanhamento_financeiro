import pyodbc


def database_connection():
    server = 'DESKTOP-98I4FGO'
    database = 'FINANCEIRO'
    user = 'Admin'
    password = '66tUa3ue'

    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + user + ';PWD=' + password)
        cursor = connection.cursor()
        print('Conexão estabelecida com sucesso!')
        return connection, cursor

    except pyodbc.Error as e:
        print('Erro ao se conectar com o banco de dados:', e)
        return None

