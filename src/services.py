import mysql.connector
from datetime import datetime


def registrar_entrada_saida(cursor, conn, nome, placa, transacao):
    if not nome or not placa or not transacao:
        print("Nome, placa e transação são obrigatórios.")
        return False

    try:
        # Verificar se o cliente existe
        cursor.execute("SELECT ID FROM CLIENTE WHERE NOME = %s", (nome,))
        cliente = cursor.fetchone()
        if not cliente:
            print("Cliente não encontrado.")
            return False
        cliente_id = cliente[0]

        # Verificar se a placa existe
        cursor.execute("SELECT ID FROM VEICULO WHERE PLACA = %s", (placa,))
        carro = cursor.fetchone()
        if not carro:
            print("Placa não encontrada.")
            return False
        carro_id = carro[0]

    
        if transacao.lower() == "entrada":
            # Verificar se já existe uma entrada sem saída para o mesmo carro e cliente
            cursor.execute("""
                SELECT COUNT(*) 
                FROM ENTRADA_SAIDA 
                WHERE ID_CARRO = %s AND ID_CLIENTE = %s AND SITUACAO = 0
            """, (carro_id, cliente_id))
            if cursor.fetchone()[0] > 0:
                print("Já existe uma entrada sem saída para este carro e cliente.")
                return False

            sql = """
                INSERT INTO ENTRADA_SAIDA (ID_CARRO, ID_CLIENTE,SITUACAO) 
                VALUES (%s, %s, 0)
            """
            valores = (carro_id, cliente_id)
        elif transacao.lower() == "saida":
            sql = """
                UPDATE ENTRADA_SAIDA 
                SET DT_HORA_SAIDA = %s 
                WHERE ID_CARRO = %s AND SIUACAO = 1
            """
            valores = (carro_id)
        else:
            print("Transação inválida. Use 'entrada' ou 'saída'.")
            return False

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
        sql_cliente = "INSERT INTO CLIENTE (NOME, TELEFONE) VALUES (%s, %s)"
        valores_cliente = (nome, telefone)
        print(f"Executando SQL: {sql_cliente} com valores {valores_cliente}")
        cursor.execute(sql_cliente, valores_cliente)
        cliente_id = cursor.lastrowid

        # Inserir carro
        sql_carro = "INSERT INTO VEICULO (MARCA, PLACA) VALUES (%s, %s)"
        valores_carro = (marca, placa)
        print(f"Executando SQL: {sql_carro} com valores {valores_carro}")
        cursor.execute(sql_carro, valores_carro)
        carro_id = cursor.lastrowid

        sql_entrada_saida = "INSERT INTO ENTRADA_SAIDA (ID_CARRO, ID_CLIENTE) VALUES (%s, %s)"
        valores_entrada_saida = (carro_id, cliente_id)
        print(f"Executando SQL: {sql_entrada_saida} com valores {valores_entrada_saida}")
        cursor.execute(sql_entrada_saida, valores_entrada_saida)

        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao inserir cliente e carro: {err}")
        return False

def verificar_placa(cursor, placa):
    try:
        sql = "SELECT COUNT(*) FROM VEICULO WHERE PLACA = %s"
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar placa: {err}")
        return False

def verificar_nome(cursor, nome):
    try:
        sql = "SELECT COUNT(*) FROM CLIENTE WHERE NOME = %s"
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
            FROM CLIENTE c
            JOIN ENTRADA_SAIDA es ON c.ID = es.ID_CLIENTE
            JOIN VEICULO ca ON es.ID_CARRO = ca.ID
            WHERE c.NOME = %s AND ca.PLACA = %s
        """
        cursor.execute(sql, (nome, placa))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar nome e placa: {err}")
        return False


def verificar_entrada_sem_saida(cursor, placa):
    try:
        sql = """
            SELECT COUNT(*) 
            FROM ENTRADA_SAIDA es
            JOIN VEICULO ca ON es.ID_CARRO = ca.ID
            WHERE ca.PLACA = %s AND es.SITUACAO = 0
            
        """
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        return result[0] == 0  # Permitir entrada se não houver registro de entrada sem saída
    except mysql.connector.Error as err:
        print(f"Erro ao verificar entrada sem saída: {err}")
        return False

def obter_dados_cliente(cursor, placa):
    try:
        sql = """
            SELECT c.NOME, c.TELEFONE, ca.MARCA, c.ID 
            FROM CLIENTE c
            JOIN ENTRADA_SAIDA es ON c.ID = es.ID_CLIENTE
            JOIN VEICULO ca ON es.ID_CARRO = ca.ID
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
                FROM CLIENTE c
                JOIN ENTRADA_SAIDA es ON c.ID = es.ID_CLIENTE
                JOIN VEICULO ca ON es.ID_CARRO = ca.ID
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