import mysql.connector
from datetime import datetime

def conectar_db():
    # Estabelece a conexão com o banco de dados.
    try:
        return mysql.connector.connect(
            host='localhost',  
            user='marina',    
            password='projeto123',  
            database='db_estacionamento' 
        )
    except mysql.connector.Error as err:
        print(f'Erro na conexão: {err}')
        return None

def registrar_entrada_saida(cursor, conn, placa, transacao):
    if not placa or not transacao:
        print("Placa e transação são obrigatórios.")
        return False

    try:
        # Verificar se a placa existe
        cursor.execute("SELECT ID FROM tb_carro WHERE PLACA = %s", (placa,))
        carro = cursor.fetchone()
        if not carro:
            print("Placa não encontrada.")
            return False

        carro_id = carro[0]
        data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if transacao.lower() == "entrada":
            sql = """
                INSERT INTO tb_entrada_saida (ID_CARRO, DT_HORA_ENTRADA) 
                VALUES (%s, %s)
            """
        elif transacao.lower() == "saida":
            sql = """
                UPDATE tb_entrada_saida 
                SET DT_HORA_SAIDA = %s 
                WHERE ID_CARRO = %s AND DT_HORA_SAIDA IS NULL
            """
        else:
            print("Transação inválida. Use 'entrada' ou 'saída'.")
            return False

        valores = (carro_id, data_hora_atual) if transacao.lower() == "entrada" else (data_hora_atual, carro_id)
        print(f"Executando SQL: {sql} com valores {valores}")
        cursor.execute(sql, valores)
        conn.commit()  # Confirma a alteração no banco

        if cursor.rowcount == 0:
            print("Nenhum registro atualizado. Verifique se a placa está correta.")
            return False

        return True

    except mysql.connector.Error as err:
        print(f"Erro ao registrar {transacao}: {err}")
        return False

def inserir_cliente_carro(cursor, conn, nome, telefone, placa, marca):
    if not nome or not telefone or not placa or not marca:
        print("Nome, telefone, placa e marca são obrigatórios.")
        return False
    try:
        # Inserir cliente
        sql_cliente = "INSERT INTO tb_cliente (NOME, TELEFONE) VALUES (%s, %s)"
        valores_cliente = (nome, telefone)
        print(f"Executando SQL: {sql_cliente} com valores {valores_cliente}")
        cursor.execute(sql_cliente, valores_cliente)
        cliente_id = cursor.lastrowid

        # Inserir carro
        sql_carro = "INSERT INTO tb_carro (MARCA, PLACA) VALUES (%s, %s)"
        valores_carro = (marca, placa)
        print(f"Executando SQL: {sql_carro} com valores {valores_carro}")
        cursor.execute(sql_carro, valores_carro)
        carro_id = cursor.lastrowid

        # Inserir entrada e saída
        data_hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_hora_saida = "Sem dados"
        sql_entrada_saida = "INSERT INTO tb_entrada_saida (ID_CARRO, ID_CLIENTE, DT_HORA_ENTRADA, DT_HORA_SAIDA) VALUES (%s, %s, %s, %s)"
        valores_entrada_saida = (carro_id, cliente_id, data_hora_entrada, data_hora_saida)
        print(f"Executando SQL: {sql_entrada_saida} com valores {valores_entrada_saida}")
        cursor.execute(sql_entrada_saida, valores_entrada_saida)

        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao inserir cliente e carro: {err}")
        return False

def verificar_placa(cursor, placa):
    try:
        sql = "SELECT COUNT(*) FROM tb_carro WHERE PLACA = %s"
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar placa: {err}")
        return False

def verificar_nome(cursor, nome):
    try:
        sql = "SELECT COUNT(*) FROM tb_cliente WHERE NOME = %s"
        cursor.execute(sql, (nome,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar nome: {err}")
        return False

def verificar_nome_placa(cursor, nome, placa):
    try:
        sql = """
            SELECT COUNT(*) 
            FROM tb_cliente c
            JOIN tb_entrada_saida es ON c.ID = es.ID_CLIENTE
            JOIN tb_carro ca ON es.ID_CARRO = ca.ID
            WHERE c.NOME = %s AND ca.PLACA = %s
        """
        cursor.execute(sql, (nome, placa))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar nome e placa: {err}")
        return False

def verificar_entrada(cursor, placa):
    try:
        sql = """
            SELECT COUNT(*) 
            FROM tb_entrada_saida es
            JOIN tb_carro ca ON es.ID_CARRO = ca.ID
            WHERE ca.PLACA = %s AND es.DT_HORA_ENTRADA IS NOT NULL
        """
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar entrada: {err}")
        return False

def verificar_saida(cursor, placa):
    try:
        sql = """
            SELECT COUNT(*) 
            FROM tb_entrada_saida es
            JOIN tb_carro ca ON es.ID_CARRO = ca.ID
            WHERE ca.PLACA = %s AND es.DT_HORA_SAIDA IS NOT NULL
        """
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar saída: {err}")
        return False

def verificar_entrada_sem_saida(cursor, placa):
    try:
        sql = """
            SELECT COUNT(*) 
            FROM tb_entrada_saida es
            JOIN tb_carro ca ON es.ID_CARRO = ca.ID
            WHERE ca.PLACA = %s AND es.DT_HORA_ENTRADA IS NOT NULL AND es.DT_HORA_SAIDA IS NULL
        """
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar entrada sem saída: {err}")
        return False

def obter_dados_cliente(cursor, placa):
    try:
        sql = """
            SELECT c.NOME, c.TELEFONE, ca.MARCA 
            FROM tb_cliente c
            JOIN tb_entrada_saida es ON c.ID = es.ID_CLIENTE
            JOIN tb_carro ca ON es.ID_CARRO = ca.ID
            WHERE ca.PLACA = %s
        """
        cursor.execute(sql, (placa,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Erro ao obter dados do cliente: {err}")
        return None

def listar_dados(conn):
    cursor = None
    try:
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.NOME, c.TELEFONE, ca.PLACA, ca.MARCA, 
                IFNULL(es.DT_HORA_ENTRADA, 'Sem dados') AS DT_HORA_ENTRADA, 
                IFNULL(es.DT_HORA_SAIDA, 'Sem dados') AS DT_HORA_SAIDA
                FROM tb_cliente c
                JOIN tb_entrada_saida es ON c.ID = es.ID_CLIENTE
                JOIN tb_carro ca ON es.ID_CARRO = ca.ID
                ORDER BY c.NOME, c.TELEFONE, ca.PLACA, ca.MARCA, es.DT_HORA_ENTRADA, es.DT_HORA_SAIDA
            """)
            entradas_saidas = cursor.fetchall()
            return {'entradas_saidas': entradas_saidas}
    except mysql.connector.Error as err:
        print(f"Erro ao listar dados: {err}")
        return {}
    finally:
        if cursor is not None:
            cursor.close()