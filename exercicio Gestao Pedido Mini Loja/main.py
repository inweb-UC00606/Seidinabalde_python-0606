import csv
import os

FICHEIRO_PRODUTOS = "produtos.csv"
FICHEIRO_PEDIDOS = "pedidos.csv"


# ---------------------------------------------------
# 1. Garantir que os ficheiros existem
# ---------------------------------------------------
def inicializar_ficheiros():
    if not os.path.exists(FICHEIRO_PRODUTOS):
        with open(FICHEIRO_PRODUTOS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nome", "preco", "stock"])

    if not os.path.exists(FICHEIRO_PEDIDOS):
        with open(FICHEIRO_PEDIDOS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["produto", "quantidade", "total"])


# ---------------------------------------------------
# 2. Carregar produtos
# ---------------------------------------------------
def carregar_produtos():
    produtos = []
    with open(FICHEIRO_PRODUTOS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            produtos.append(linha)
    return produtos


# ---------------------------------------------------
# 3. Guardar produtos
# ---------------------------------------------------
def guardar_produtos(produtos):
    with open(FICHEIRO_PRODUTOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "preco", "stock"])
        for p in produtos:
            writer.writerow([p["nome"], p["preco"], p["stock"]])


# ---------------------------------------------------
# 4. Registar produto
# ---------------------------------------------------
def registar_produto(produtos):
    print("\n--- Registar Produto ---")

    nome = input("Nome: ").strip()
    if nome == "":
        print("Erro: nome não pode estar vazio.")
        return

    # verificar duplicados
    for p in produtos:
        if p["nome"].lower() == nome.lower():
            print("Erro: produto já existe.")
            return

    preco = input("Preço: ").strip()
    if not preco.replace(".", "", 1).isdigit():
        print("Erro: preço inválido.")
        return

    stock = input("Stock inicial: ").strip()
    if not stock.isdigit():
        print("Erro: stock deve ser inteiro.")
        return

    produtos.append({"nome": nome, "preco": preco, "stock": stock})
    guardar_produtos(produtos)

    print("Produto registado com sucesso!")


# ---------------------------------------------------
# 5. Listar produtos (tabela alinhada)
# ---------------------------------------------------
def listar_produtos(produtos):
    print("\n--- Lista de Produtos ---")

    if not produtos:
        print("Nenhum produto registado.")
        return

    # calcular larguras
    max_nome = max(len(p["nome"]) for p in produtos)
    max_preco = max(len(p["preco"]) for p in produtos)
    max_stock = max(len(p["stock"]) for p in produtos)

    largura = max_nome + max_preco + max_stock + 10

    print("-" * largura)
    print(f"| {'Nome'.ljust(max_nome)} | {'Preço'.ljust(max_preco)} | {'Stock'.ljust(max_stock)} |")
    print("-" * largura)

    for p in produtos:
        print(f"| {p['nome'].ljust(max_nome)} | {p['preco'].ljust(max_preco)} | {p['stock'].ljust(max_stock)} |")

    print("-" * largura)


# ---------------------------------------------------
# 6. Fazer pedido
# ---------------------------------------------------
def fazer_pedido(produtos):
    print("\n--- Fazer Pedido ---")

    listar_produtos(produtos)

    nome = input("Nome do produto: ").strip()

    # procurar produto
    produto = None
    for p in produtos:
        if p["nome"].lower() == nome.lower():
            produto = p
            break

    if produto is None:
        print("Erro: produto não encontrado.")
        return

    quantidade = input("Quantidade: ").strip()
    if not quantidade.isdigit():
        print("Erro: quantidade inválida.")
        return

    quantidade = int(quantidade)
    stock_atual = int(produto["stock"])

    if quantidade > stock_atual:
        print("Erro: stock insuficiente.")
        return

    preco = float(produto["preco"])
    total = preco * quantidade

    # atualizar stock
    produto["stock"] = str(stock_atual - quantidade)
    guardar_produtos(produtos)

    # guardar pedido
    with open(FICHEIRO_PEDIDOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([produto["nome"], quantidade, total])

    print(f"Pedido registado! Total: {total:.2f}€")


# ---------------------------------------------------
# 7. Mostrar pedidos
# ---------------------------------------------------
def mostrar_pedidos():
    print("\n--- Lista de Pedidos ---")

    with open(FICHEIRO_PEDIDOS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        pedidos = list(reader)

    if not pedidos:
        print("Nenhum pedido registado.")
        return

    for p in pedidos:
        print(f"Produto: {p['produto']} | Quantidade: {p['quantidade']} | Total: {p['total']}€")


# ---------------------------------------------------
# 8. Menu
# ---------------------------------------------------
def menu():
    print("\n===== MENU =====")
    print("1 - Registar produto")
    print("2 - Listar produtos")
    print("3 - Fazer pedido")
    print("4 - Mostrar pedidos")
    print("0 - Sair")


# ---------------------------------------------------
# 9. Programa principal
# ---------------------------------------------------
def main():
    inicializar_ficheiros()
    produtos = carregar_produtos()

    while True:
        menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            registar_produto(produtos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            fazer_pedido(produtos)
        elif opcao == "4":
            mostrar_pedidos()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()