from flask import Flask, request, jsonify, send_from_directory
from services import conectar_db, registrar_entrada_saida, listar_dados, inserir_cliente_carro, verificar_placa, verificar_nome_placa, verificar_nome, verificar_entrada, verificar_saida, obter_dados_cliente, verificar_entrada_sem_saida
import os
from datetime import datetime
import unicodedata
from src import app

def get_db_connection():
    conn = conectar_db()
    if conn.is_connected():
        return conn
    else:
        raise Exception("Erro ao conectar ao banco de dados")

def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/registrar_entrada_saida', methods=['POST'])
def api_registrar_entrada_saida():
    data = request.json
    placa = data.get('placa')
    transacao = data.get('transacao')
    horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Recebido para registrar_entrada_saida: placa={placa}, transacao={transacao}, horario={horario}")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if transacao.lower() == "entrada":
            # Verificar se há um registro de entrada sem saída antes de permitir a entrada
            if verificar_entrada_sem_saida(cursor, placa):
                return jsonify({'message': 'O veículo já está registrado como entrada sem saída'}), 400

            # Registrar a entrada
            if registrar_entrada_saida(cursor, conn, placa, transacao):
                conn.commit()
                return jsonify({'message': 'Entrada registrada com sucesso!'}), 200
            else:
                conn.rollback()
                return jsonify({'message': 'Erro ao registrar entrada.'}), 500

        elif transacao.lower() == "saida":
            # Verificar se há um registro de entrada sem saída antes de permitir a saída
            if verificar_entrada_sem_saida(cursor, placa):
                # Registrar a saída
                if registrar_entrada_saida(cursor, conn, placa, transacao):
                    conn.commit()
                    return jsonify({'message': 'Saída registrada com sucesso!'}), 200
                else:
                    conn.rollback()
                    return jsonify({'message': 'Erro ao registrar saída.'}), 500
            else:
                return jsonify({'message': 'O veículo não tem registro de entrada ou já tem registro de saída'}), 400

        return jsonify({'message': 'Transação inválida.'}), 400
    except Exception as e:
        conn.rollback()
        print(f"Erro ao registrar {transacao}: {e}")
        return jsonify({'message': f'Erro ao registrar {transacao}.'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/inserir_cliente_carro', methods=['POST'])
def api_inserir_cliente_carro():
    data = request.json
    nome = normalize_string(data.get('nome'))
    telefone = data.get('telefone')
    placa = data.get('placa')
    marca = data.get('marca')
    data_hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_hora_saida = "Sem dados"
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Inserir cliente e carro
        if inserir_cliente_carro(cursor, conn, nome, telefone, placa, marca):
            conn.commit()
            return jsonify({'message': 'Cliente e carro inseridos com sucesso!'}), 200
        else:
            conn.rollback()
            return jsonify({'message': 'Erro ao inserir cliente e carro.'}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir cliente e carro: {e}")
        return jsonify({'message': 'Erro ao inserir cliente e carro.'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registrar_entrada', methods=['POST'])
def api_registrar_entrada():
    data = request.json
    placa = data.get('placa')
    horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Recebido para registrar entrada: placa={placa}, horario={horario}")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar se há um registro de saída antes de permitir a entrada
        if not verificar_saida(cursor, placa):
            return jsonify({'message': 'O veículo não tem registro de saída'}), 400

        # Obter dados do cliente existente
        cliente = obter_dados_cliente(cursor, placa)
        if cliente:
            nome = cliente[0]
            telefone = cliente[1]
            marca = cliente[2]
            # Inserir novo cadastro com os dados existentes e a nova data de entrada
            if registrar_entrada_saida(cursor, conn, placa, "entrada"):
                conn.commit()
                return jsonify({'message': 'Entrada registrada com sucesso!'}), 200
            else:
                conn.rollback()
                return jsonify({'message': 'Erro ao registrar entrada.'}), 500
        else:
            return jsonify({'message': 'Erro ao obter dados do cliente.'}), 500
    except Exception as e:
        conn.rollback()
        print(f"Erro ao registrar entrada: {e}")
        return jsonify({'message': 'Erro ao registrar entrada.'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/verificar_placa', methods=['GET'])
def api_verificar_placa():
    placa = request.args.get('placa')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        exists = verificar_placa(cursor, placa)
        return jsonify({'exists': exists}), 200
    except Exception as e:
        print(f"Erro ao verificar placa: {e}")
        return jsonify({'exists': False}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/verificar_nome', methods=['GET'])
def api_verificar_nome():
    nome = normalize_string(request.args.get('nome'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        exists = verificar_nome(cursor, nome)
        return jsonify({'exists': exists}), 200
    except Exception as e:
        print(f"Erro ao verificar nome: {e}")
        return jsonify({'exists': False}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/verificar_nome_placa', methods=['GET'])
def api_verificar_nome_placa():
    nome = normalize_string(request.args.get('nome'))
    placa = request.args.get('placa')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        exists = verificar_nome_placa(cursor, nome, placa)
        return jsonify({'exists': exists}), 200
    except Exception as e:
        print(f"Erro ao verificar nome e placa: {e}")
        return jsonify({'exists': False}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/verificar_entrada', methods=['GET'])
def api_verificar_entrada():
    placa = request.args.get('placa')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        exists = verificar_entrada(cursor, placa)
        return jsonify({'exists': exists}), 200
    except Exception as e:
        print(f"Erro ao verificar entrada: {e}")
        return jsonify({'exists': False}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/verificar_saida', methods=['GET'])
def api_verificar_saida():
    placa = request.args.get('placa')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        exists = verificar_saida(cursor, placa)
        return jsonify({'exists': exists}), 200
    except Exception as e:
        print(f"Erro ao verificar saída: {e}")
        return jsonify({'exists': False}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/listar_dados', methods=['GET'])
def api_listar_dados():
    conn = get_db_connection()
    try:
        dados = listar_dados(conn)
        return jsonify(dados), 200
    except Exception as e:
        print(f"Erro ao listar dados: {e}")
        return jsonify({}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
