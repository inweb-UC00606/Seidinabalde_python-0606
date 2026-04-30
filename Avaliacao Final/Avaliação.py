# ---------------------------------------------
# SISTEMA DE GINÁSIOS
# ---------------------------------------------

clientes = []
treinadores = []
aulas = []
ginasios = []

PLANOS = {
    "basic": {"limite": 3, "mensalidade": 30.50},
    "full": {"limite": 10, "mensalidade": 50.00},
    "premium": {"limite": 9999, "mensalidade": 70.00}
}

# ---------------------------------------------
# CLIENTES
# ---------------------------------------------

def registar_cliente():
    cc = input("CC: ")
    nif = input("NIF: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    nome = input("Nome: ")
    morada = input("Morada: ")
    idade = int(input("Idade: "))

    if idade < 18:
        print("Cliente menor de idade. Não pode inscrever-se.")
        return

    plano = input("Plano (basic/full/premium): ").lower()
    ginasio = input("Ginásio que pretende frequentar: ")

    cliente = {
        "cc": cc,
        "nif": nif,
        "email": email,
        "telefone": telefone,
        "nome": nome,
        "morada": morada,
        "idade": idade,
        "plano": plano,
        "ginasio": ginasio,
        "aulas_inscritas": 0
    }

    clientes.append(cliente)
    print("Cliente registado com sucesso!")


def remover_cliente():
    nif = input("NIF do cliente a remover: ")
    for c in clientes:
        if c["nif"] == nif:
            clientes.remove(c)
            print("Cliente removido com sucesso.")
            return
    print("Cliente não encontrado.")


def alterar_plano():
    nif = input("NIF do cliente: ")
    for c in clientes:
        if c["nif"] == nif:
            novo = input("Novo plano (basic/full/premium): ")
            c["plano"] = novo
            print("Plano alterado.")
            return
    print("Cliente não encontrado.")


# ---------------------------------------------
# TREINADORES
# ---------------------------------------------

def registar_treinador():
    nif = input("NIF: ")
    nome = input("Nome: ")
    morada = input("Morada: ")
    telefone = input("Telefone: ")
    modalidades = input("Modalidades (separadas por vírgula): ").split(",")
    ginasio = input("Ginásio onde trabalha: ")

    treinador = {
        "nif": nif,
        "nome": nome,
        "morada": morada,
        "telefone": telefone,
        "modalidades": modalidades,
        "ginasio": ginasio,
        "ativo": True
    }

    treinadores.append(treinador)
    print("Treinador registado.")


def inativar_treinador():
    nif = input("NIF do treinador: ")
    for t in treinadores:
        if t["nif"] == nif:
            t["ativo"] = False
            print("Treinador inativado.")
            return
    print("Treinador não encontrado.")


# ---------------------------------------------
# AULAS
# ---------------------------------------------

def registar_aula():
    nif = input("NIF do treinador: ")

    treinador = None
    for t in treinadores:
        if t["nif"] == nif and t["ativo"]:
            treinador = t

    if treinador is None:
        print("Treinador não encontrado ou inativo.")
        return

    dia = int(input("Dia: "))
    mes = int(input("Mês: "))
    ano = int(input("Ano: "))
    modalidade = input("Modalidade: ")

    aula = {
        "treinador": treinador,
        "dia": dia,
        "mes": mes,
        "ano": ano,
        "modalidade": modalidade,
        "ginasio": treinador["ginasio"],
        "clientes": []
    }

    aulas.append(aula)
    print("Aula registada.")


def remover_aula():
    modalidade = input("Modalidade da aula a remover: ")
    for a in aulas:
        if a["modalidade"] == modalidade:
            aulas.remove(a)
            print("Aula removida.")
            return
    print("Aula não encontrada.")


def alterar_data_aula():
    modalidade = input("Modalidade da aula: ")
    for a in aulas:
        if a["modalidade"] == modalidade:
            a["dia"] = int(input("Novo dia: "))
            a["mes"] = int(input("Novo mês: "))
            a["ano"] = int(input("Novo ano: "))
            print("Data alterada.")
            return
    print("Aula não encontrada.")


# ---------------------------------------------
# GINÁSIOS
# ---------------------------------------------

def registar_ginasio():
    gerente = input("Gerente: ")
    localidade = input("Localidade: ")
    telefone = input("Telefone: ")

    g = {
        "gerente": gerente,
        "localidade": localidade,
        "telefone": telefone
    }

    ginasios.append(g)
    print("Ginásio registado.")


# ---------------------------------------------
# LISTAGENS DE AULAS GINASIO/TREINADORES
# ---------------------------------------------

def listar_aulas_ginasio():
    g = input("Nome/localidade do ginásio: ")
    for a in aulas:
        if a["ginasio"] == g:
            print(f"{a['dia']}/{a['mes']}/{a['ano']} - {a['modalidade']} - Treinador: {a['treinador']['nome']} - Clientes: {len(a['clientes'])}")


def listar_aulas_treinador():
    nif = input("NIF do treinador: ")
    for a in aulas:
        if a["treinador"]["nif"] == nif:
            print(f"{a['dia']}/{a['mes']}/{a['ano']} - {a['modalidade']}")


# ---------------------------------------------
# INSCRIÇÃO DE CLIENTE
# ---------------------------------------------

def inscrever_cliente():
    nif = input("NIF do cliente: ")

    cliente = None
    for c in clientes:
        if c["nif"] == nif:
            cliente = c

    if cliente is None:
        print("Cliente não encontrado.")
        return

    modalidade = input("Modalidade da aula: ")

    aula = None
    for a in aulas:
        if a["modalidade"] == modalidade and a["ginasio"] == cliente["ginasio"]:
            aula = a

    if aula is None:
        print("Aula não encontrada no ginásio do cliente.")
        return

    # Verificar limite do plano
    limite = PLANOS[cliente["plano"]]["limite"]

    if cliente["aulas_inscritas"] >= limite:
        print("Cliente excedeu o limite do plano. Atualizando automaticamente...")

        if cliente["aulas_inscritas"] > 10:
            cliente["plano"] = "premium"
        elif cliente["aulas_inscritas"] > 3:
            cliente["plano"] = "full"

    aula["clientes"].append(cliente)
    cliente["aulas_inscritas"] += 1
    print("Cliente inscrito com sucesso!")


# ---------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------

while True:
    print("""
1 - Registar Cliente
2 - Remover Cliente
3 - Alterar plano de Cliente
4 - Registar Treinador
5 - Inactivar Treinador
6 - Registar Aula
7 - Alterar Aula
   1 - Remover
   2 - Alterar Data
8 - Registar Ginásio
9 - Lista de Aulas de um Ginásio
10 - Lista de Aulas de Treinador
11 - Inscrição de Cliente em Aula
0 - Sair
""")

    op = input("Opção: ")

    if op == "1": registar_cliente()
    elif op == "2": remover_cliente()
    elif op == "3": alterar_plano()
    elif op == "4": registar_treinador()
    elif op == "5": inativar_treinador()
    elif op == "6": registar_aula()
    elif op == "7":
        sub = input("1 - Remover | 2 - Alterar Data: ")
        if sub == "1": remover_aula()
        else: alterar_data_aula()
    elif op == "8": registar_ginasio()
    elif op == "9": listar_aulas_ginasio()
    elif op == "10": listar_aulas_treinador()
    elif op == "11": inscrever_cliente()
    elif op == "0":
        print("A sair...")
        break
    else:
        print("Opção inválida.")