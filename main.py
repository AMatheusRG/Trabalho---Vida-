import sqlite3
import os
import csv
import json

# Criar pasta db/ se não existir
os.makedirs('db', exist_ok=True)

# Caminho do banco de dados
DB_PATH = 'db/vida_mais.db'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função de criação de tabelas
def criar_tabelas():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crm TEXT NOT NULL,
            especialidade TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            medico_id INTEGER,
            data TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id)
        )
    ''')

    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas criadas com sucesso!")

# Funcao para importar os medicos do arquivo csv com o DictReader, que transforma o conteudo em lista de Dicionarios
def importar_medicos(csv_path):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    with open(csv_path, 'r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            cursor.execute('''
                INSERT INTO medicos (nome, crm, especialidade)
                VALUES (?, ?, ?)
            ''', (linha['nome'], linha['crm'], linha['especialidade']))
    
    conexao.commit()
    conexao.close()
    print("Médicos importados com sucesso.")

# Funcao para importar os pacientes do arquivo json com o Load, que transforma o conteudo em lista de Dicionarios
def importar_pacientes(json_path):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    with open(json_path, 'r', encoding='utf-8') as arquivo:
        pacientes = json.load(arquivo)
        for paciente in pacientes:
            cursor.execute('''
                INSERT INTO pacientes (nome, cpf, data_nascimento, telefone)
                VALUES (?, ?, ?, ?)
            ''', (paciente['nome'], paciente['cpf'], paciente['data_nascimento'], paciente['telefone']))
    
    conexao.commit()
    conexao.close()
    print("Pacientes importados com sucesso.")

# Permite o cadastro de medicos manualmente pelo terminal
def cadastrar_medico():
    nome = input("Nome do médico: ")
    crm = input("CRM: ")
    especialidade = input("Especialidade: ")

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO medicos (nome, crm, especialidade)
        VALUES (?, ?, ?)
    ''', (nome, crm, especialidade))
    conexao.commit()
    conexao.close()
    print("Médico cadastrado com sucesso!")

# Permite o cadastro de pacientes manualmente pelo terminal    
def cadastrar_paciente():
    nome = input("Nome do paciente: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone: ")

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO pacientes (nome, cpf, data_nascimento, telefone)
        VALUES (?, ?, ?, ?)
    ''', (nome, cpf, data_nascimento, telefone))
    conexao.commit()
    conexao.close()
    print("Paciente cadastrado com sucesso!")    

# Permite que o usuario agende consultas informando dados
def agendar_consulta():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # Mostrar pacientes
    print("\n--- Pacientes ---")
    cursor.execute("SELECT id, nome FROM pacientes")
    for paciente in cursor.fetchall():
        print(f"{paciente[0]} - {paciente[1]}")

    paciente_id = input("ID do paciente: ")

    # Mostrar médicos
    print("\n--- Médicos ---")
    cursor.execute("SELECT id, nome, especialidade FROM medicos")
    for medico in cursor.fetchall():
        print(f"{medico[0]} - {medico[1]} ({medico[2]})")

    medico_id = input("ID do médico: ")

    data = input("Data da consulta (AAAA-MM-DD): ")
    observacoes = input("Observações (opcional): ")

    cursor.execute('''
        INSERT INTO consultas (paciente_id, medico_id, data, observacoes)
        VALUES (?, ?, ?, ?)
    ''', (paciente_id, medico_id, data, observacoes))

    conexao.commit()
    conexao.close()
    print("Consulta agendada com sucesso!")

# Mostrar no terminal todas as consultas de um paciente, incluindo seus dados
def listar_consultas_por_paciente():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # Exibir pacientes disponíveis
    print("\n--- Pacientes ---")
    cursor.execute("SELECT id, nome FROM pacientes")
    pacientes = cursor.fetchall()
    for paciente in pacientes:
        print(f"{paciente[0]} - {paciente[1]}")

    paciente_id = input("Digite o ID do paciente: ")

    print(f"\nConsultas do paciente ID {paciente_id}:\n")

    # Para esse paciente, quais foram as consultas, com qual médico, em que data, e com quais observações.
    cursor.execute('''
        SELECT c.data, c.observacoes, m.nome, m.especialidade
        FROM consultas c
        JOIN medicos m ON c.medico_id = m.id
        WHERE c.paciente_id = ?
        ORDER BY c.data
    ''', (paciente_id,))

    consultas = cursor.fetchall()

    # Se nenhuma consulta for encontrada, exibe mensagem, senao entra no loop for
    if not consultas:
        print("Nenhuma consulta encontrada para esse paciente.")
    else:
        for consulta in consultas:
            data, observacoes, medico_nome, especialidade = consulta
            print(f"Data: {data}")
            print(f"Médico: {medico_nome} ({especialidade})")
            print(f"Observações: {observacoes}\n")

    conexao.close()

# Mostrar no terminal quantas consultas cada medico realizou, com suas especificacoes
def relatorio_consultas_por_medico():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # Foi dificil aprender left join, mas ele garante que medicos sem nenhuma consulta, tambem aparecam no relatorio
    cursor.execute('''
        SELECT m.nome, m.especialidade, COUNT(c.id) as total_consultas
        FROM medicos m
        LEFT JOIN consultas c ON c.medico_id = m.id
        GROUP BY m.id
        ORDER BY total_consultas DESC
    ''')

    resultados = cursor.fetchall()

    print("\n--- RELATÓRIO: Consultas por Médico ---")
    for nome, especialidade, total in resultados:
        print(f"Médico: {nome} ({especialidade}) - {total} consulta(s)")

    conexao.close()

def exportar_relatorio_consultas_csv():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT m.nome, m.especialidade, COUNT(c.id) as total_consultas
        FROM medicos m
        LEFT JOIN consultas c ON c.medico_id = m.id
        GROUP BY m.id
        ORDER BY total_consultas DESC
    ''')

    resultados = cursor.fetchall()
    conexao.close()

    # Garante que a pasta relatorios/ exista
    os.makedirs('relatorios', exist_ok=True)

    # Caminho do arquivo CSV
    caminho_csv = 'relatorios/consultas_por_medico.csv'

    # Abre (ou cria) o arquivo CSV para escrita, o newline evita linhas em branco extras
    with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(['Nome do Médico', 'Especialidade', 'Total de Consultas'])  # Cabeçalho
        
        # Percorre os resultados do banco e escreve cada linha no CSV com esses dados
        for nome, especialidade, total in resultados:
            escritor.writerow([nome, especialidade, total])

    print(f"Relatório exportado com sucesso para {caminho_csv}")
    
def menu():
    while True:
        limpar_tela()
        print("=" * 40)
        print("      SISTEMA CLÍNICA VIDA+      ")
        print("=" * 40)
        print("1. Cadastrar médico")
        print("2. Cadastrar paciente")
        print("3. Agendar consulta")
        print("4. Listar consultas de um paciente")
        print("5. Relatório: consultas por médico (terminal)")
        print("6. Exportar relatório CSV")
        print("7. Sair")
        print("=" * 40)

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            limpar_tela()
            cadastrar_medico()
        elif escolha == '2':
            limpar_tela()
            cadastrar_paciente()
        elif escolha == '3':
            limpar_tela()
            agendar_consulta()
        elif escolha == '4':
            limpar_tela()
            listar_consultas_por_paciente()
        elif escolha == '5':
            limpar_tela()
            relatorio_consultas_por_medico()
        elif escolha == '6':
            limpar_tela()
            exportar_relatorio_consultas_csv()
        elif escolha == '7':
            print("\nEncerrando o sistema. Até logo!")
            break
        else:
            print("\n⚠️ Opção inválida. Tente novamente.")

        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    criar_tabelas()
    # Verifica se as tabelas estão vazias antes de importar
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM medicos")
    total_medicos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total_pacientes = cursor.fetchone()[0]

    conexao.close()

    if total_medicos == 0:
        importar_medicos('dados/medicos.csv')

    if total_pacientes == 0:
        importar_pacientes('dados/pacientes.json')

    menu()