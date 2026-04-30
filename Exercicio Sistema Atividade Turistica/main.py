import csv
import os

# ----------------- Constantes -----------------

FICHEIRO_ATIVIDADES = "atividades.csv"
FICHEIRO_CLIENTES = "clientes.csv"
FICHEIRO_RESERVAS = "reservas.csv"

CAB_ATIVIDADES = ["id_atividade", "nome", "local", "preco", "vagas"]
CAB_CLIENTES = ["id_cliente", "nome", "contacto"]
CAB_RESERVAS = [
    "id_reserva",
    "id_cliente",
    "nome_cliente",
    "id_atividade",
    "nome_atividade",
    "quantidade_pessoas",
    "total"
]

# ----------------- Ficheiros -----------------

def ficheiro_existe_ou_cria(nome, cab):
    if not os.path.exists(nome):
        with open(nome, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(cab)

def ler_todos(nome):
    if not os.path.exists(nome):
        return []
    try:
        with open(nome, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f, delimiter=";"))
    except:
        print("Erro ao ler ficheiro.")
        return []

def escrever_todos(nome, cab, dados):
    with open(nome, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cab, delimiter=";")
        writer.writeheader()
        writer.writerows(dados)

def acrescentar(nome, cab, linha):
    ficheiro_existe_ou_cria(nome, cab)
    with open(nome, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cab, delimiter=";")
        writer.writerow(linha)

# ----------------- Tabela -----------------

def imprimir_tabela(lista, titulo=""):
    if not lista:
        print(f"\n{titulo} (sem dados)\n")
        return

    print(f"\n{titulo}")
    chaves = lista[0].keys()
    for l in lista:
        print(" | ".join(str(l[c]) for c in chaves))
    print()

# ----------------- Atividades -----------------

def registar_atividade():
    print("\n--- Registar Atividade ---")
    atividades = ler_todos(FICHEIRO_ATIVIDADES)

    id_atividade = input("ID: ").strip()
    if not id_atividade:
        print("ID obrigatório.")
        return
    if any(a["id_atividade"] == id_atividade for a in atividades):
        print("ID já existe.")
        return

    nome = input("Nome: ").strip()
    local = input("Local: ").strip()

    try:
        preco = float(input("Preço (€): "))
        if preco < 0:
            print("Preço inválido.")
            return
    except:
        print("Preço inválido.")
        return

    try:
        vagas = int(input("Vagas: "))
        if vagas < 0:
            print("Vagas inválidas.")
            return
    except:
        print("Vagas inválidas.")
        return

    nova = {
        "id_atividade": id_atividade,
        "nome": nome,
        "local": local,
        "preco": str(preco),
        "vagas": str(vagas)
    }

    acrescentar(FICHEIRO_ATIVIDADES, CAB_ATIVIDADES, nova)
    print("✔ Atividade registada.")

def listar_atividades():
    imprimir_tabela(ler_todos(FICHEIRO_ATIVIDADES), "Atividades")

# ----------------- Clientes -----------------

def registar_cliente():
    print("\n--- Registar Cliente ---")
    clientes = ler_todos(FICHEIRO_CLIENTES)

    id_cliente = input("ID: ").strip()
    if not id_cliente:
        print("ID obrigatório.")
        return
    if any(c["id_cliente"] == id_cliente for c in clientes):
        print("ID já existe.")
        return

    nome = input("Nome: ").strip()
    contacto = input("Contacto: ").strip()

    novo = {
        "id_cliente": id_cliente,
        "nome": nome,
        "contacto": contacto
    }

    acrescentar(FICHEIRO_CLIENTES, CAB_CLIENTES, novo)
    print("✔ Cliente registado.")

def listar_clientes():
    imprimir_tabela(ler_todos(FICHEIRO_CLIENTES), "Clientes")

# ----------------- Reservas -----------------

def obter_atividade(id_a):
    for a in ler_todos(FICHEIRO_ATIVIDADES):
        if a["id_atividade"] == id_a:
            return a
    return None

def obter_cliente(id_c):
    for c in ler_todos(FICHEIRO_CLIENTES):
        if c["id_cliente"] == id_c:
            return c
    return None

def atualizar_atividade(a_nova):
    lista = ler_todos(FICHEIRO_ATIVIDADES)
    for i, a in enumerate(lista):
        if a["id_atividade"] == a_nova["id_atividade"]:
            lista[i] = a_nova
    escrever_todos(FICHEIRO_ATIVIDADES, CAB_ATIVIDADES, lista)

def efetuar_reserva():
    print("\n--- Reserva ---")
    reservas = ler_todos(FICHEIRO_RESERVAS)

    id_reserva = input("ID reserva: ").strip()
    if not id_reserva:
        print("ID obrigatório.")
        return
    if any(r["id_reserva"] == id_reserva for r in reservas):
        print("ID já existe.")
        return

    id_cliente = input("ID cliente: ").strip()
    cliente = obter_cliente(id_cliente)
    if not cliente:
        print("Cliente não existe.")
        return

    id_atividade = input("ID atividade: ").strip()
    atividade = obter_atividade(id_atividade)
    if not atividade:
        print("Atividade não existe.")
        return

    try:
        qtd = int(input("Quantidade pessoas: "))
        if qtd <= 0:
            print("Quantidade inválida.")
            return
    except:
        print("Quantidade inválida.")
        return

    vagas = int(atividade["vagas"])
    if qtd > vagas:
        print("Sem vagas suficientes.")
        return

    preco = float(atividade["preco"])
    total = qtd * preco

    nova = {
        "id_reserva": id_reserva,
        "id_cliente": id_cliente,
        "nome_cliente": cliente["nome"],
        "id_atividade": id_atividade,
        "nome_atividade": atividade["nome"],
        "quantidade_pessoas": str(qtd),
        "total": f"{total:.2f}"
    }

    acrescentar(FICHEIRO_RESERVAS, CAB_RESERVAS, nova)

    atividade["vagas"] = str(vagas - qtd)
    atualizar_atividade(atividade)

    print(f"✔ Reserva feita. Total: {total:.2f}€")

def listar_reservas():
    imprimir_tabela(ler_todos(FICHEIRO_RESERVAS), "Reservas")

# ----------------- Menu -----------------

def menu():
    while True:
        print("\n1-Atividades 2-Listar A 3-Clientes 4-Listar C 5-Reserva 6-Listar R 0-Sair")
        op = input("Opção: ")

        if op == "1": registar_atividade()
        elif op == "2": listar_atividades()
        elif op == "3": registar_cliente()
        elif op == "4": listar_clientes()
        elif op == "5": efetuar_reserva()
        elif op == "6": listar_reservas()
        elif op == "0": break
        else: print("Opção inválida.")

# ----------------- Start -----------------

if __name__ == "__main__":
    ficheiro_existe_ou_cria(FICHEIRO_ATIVIDADES, CAB_ATIVIDADES)
    ficheiro_existe_ou_cria(FICHEIRO_CLIENTES, CAB_CLIENTES)
    ficheiro_existe_ou_cria(FICHEIRO_RESERVAS, CAB_RESERVAS)
    menu()