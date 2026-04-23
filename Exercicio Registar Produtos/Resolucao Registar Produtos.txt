FICHEIRO = "produtos.txt"


# ---------------------------------------------------
# 1. Carregar produtos do ficheiro ao iniciar
# ---------------------------------------------------
def carregar_produtos():
    produtos = []
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("|") or linha.startswith("-"):
                    continue  # ignora linhas da tabela
                partes = linha.split(";")
                if len(partes) == 3:
                    produtos.append(partes)
    except FileNotFoundError:
        pass
    return produtos


# ---------------------------------------------------
# 2. Reescrever o ficheiro como tabela alinhada
# ---------------------------------------------------
def guardar_ficheiro_tabela(produtos):

    if not produtos:
        with open(FICHEIRO, "w", encoding="utf-8") as f:
            f.write("Nenhum produto registado.\n")
        return

    # calcular larguras automáticas
    max_nome = max(max(len(p[0]) for p in produtos), len("Nome"))
    max_preco = max(max(len(p[1]) for p in produtos), len("Preço (€)"))
    max_qtd = max(max(len(p[2]) for p in produtos), len("Qtd"))

    largura_total = max_nome + max_preco + max_qtd + 10

    with open(FICHEIRO, "w", encoding="utf-8") as f:
        f.write("-" * largura_total + "\n")
        f.write(f"| {'Nome'.ljust(max_nome)} | {'Preço (€)'.ljust(max_preco)} | {'Qtd'.ljust(max_qtd)} |\n")
        f.write("-" * largura_total + "\n")

        for nome, preco, quantidade in produtos:
            f.write(f"| {nome.ljust(max_nome)} | {preco.ljust(max_preco)} | {quantidade.ljust(max_qtd)} |\n")

        f.write("-" * largura_total + "\n")


# ---------------------------------------------------
# 3. Inserir produto
# ---------------------------------------------------
def inserir_produto(produtos):
    nome = input("Nome do produto: ").strip()
    if nome.lower() == "sair":
        return

    preco = input("Preço: ").strip()
    quantidade = input("Quantidade: ").strip()

    produtos.append([nome, preco, quantidade])
    guardar_ficheiro_tabela(produtos)

    print("Produto guardado com sucesso!\n")


# ---------------------------------------------------
# 4. Mostrar tabela na consola
# ---------------------------------------------------
def listar_produtos(produtos):
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            print("\n" + f.read())
    except FileNotFoundError:
        print("Ainda não existem produtos guardados.")


# ---------------------------------------------------
# 5. Menu
# ---------------------------------------------------
def menu():
    print("\n===== MENU =====")
    print("1 - Inserir produto")
    print("2 - Listar produtos")
    print("0 - Sair")


# ---------------------------------------------------
# 6. Programa principal
# ---------------------------------------------------
def main():
    produtos = carregar_produtos()

    # garantir que o ficheiro começa formatado
    guardar_ficheiro_tabela(produtos)

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            inserir_produto(produtos)

        elif opcao == "2":
            listar_produtos(produtos)

        elif opcao == "0":
            print("A sair do programa... Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()