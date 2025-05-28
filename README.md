# 🏥 Clínica Vida+ – Sistema em Python

Este é um projeto acadêmico desenvolvido para a disciplina **Desenvolvimento Rápido em Python**, com o objetivo de simular um sistema local de gestão para uma clínica popular.

---

## 🎯 Objetivo

Substituir o processo manual de fichas de pacientes e médicos por um sistema digital simples, funcional e de baixo custo. O sistema permite:

- Cadastro de médicos e pacientes
- Agendamento de consultas
- Relatórios e exportações
- Persistência dos dados com SQLite

---

## 🧱 Tecnologias utilizadas

- Python
- SQLite (`sqlite3`)
- JSON e CSV
- Interface via terminal

---

## 🗃️ Estrutura do banco de dados

O banco (`vida_mais.db`) possui 3 tabelas:

- `medicos(id, nome, crm, especialidade)`
- `pacientes(id, nome, cpf, data_nascimento, telefone)`
- `consultas(id, paciente_id, medico_id, data, observacoes)`

---

## 📂 Estrutura de pastas

clinica-vida-mais/
├── main.py
├── dados/
│ ├── medicos.csv
│ └── pacientes.json
├── db/
│ └── vida_mais.db
├── relatorios/
│ └── consultas_por_medico.csv
├── .gitignore
└── README.md

---

## ▶️ Como executar

1. Clone o repositório:
   git clone https://github.com/AMatheusRG/clinica-vida-mais.git

2. Entre na pasta:
    cd clinica-vida-mais

3. Execute:
    python main.py

4. Use o menu no terminal para interagir com o sistema.