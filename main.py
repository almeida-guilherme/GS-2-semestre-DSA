from servico import Servico, CATEGORIAS
from lista import ListaEncadeada
from dados_exemplo import gerar_exemplos


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        entrada = input(mensagem).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue

        if minimo is not None and valor < minimo:
            print(f"O valor precisa ser no mínimo {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"O valor precisa ser no máximo {maximo}.")
            continue
        return valor


def ler_texto(mensagem, obrigatorio=True):
    while True:
        texto = input(mensagem).strip()
        if texto or not obrigatorio:
            return texto
        print("Esse campo não pode ficar vazio.")


def escolher_categoria(permitir_manter=False):
    print("Categorias:")
    for i, categoria in enumerate(CATEGORIAS, start=1):
        print(f"  {i} - {categoria}")

    if permitir_manter:
        opcao = ler_inteiro("Escolha a categoria (0 para manter): ", 0, len(CATEGORIAS))
        if opcao == 0:
            return ""
    else:
        opcao = ler_inteiro("Escolha a categoria: ", 1, len(CATEGORIAS))
    return CATEGORIAS[opcao - 1]


def mostrar_lista(servicos):
    for servico in servicos:
        print(" ", servico.resumo())


def cadastrar(lista):
    print("\n--- Cadastrar serviço ---")
    id_novo = ler_inteiro("ID: ", 1)
    if lista.buscar_por_id(id_novo) is not None:
        print(f"Já existe um serviço com o ID {id_novo}. Cadastro cancelado.")
        return

    titulo = ler_texto("Título: ")
    categoria = escolher_categoria()
    descricao = ler_texto("Descrição: ")
    requisitos = ler_texto("Requisitos: ")
    local = ler_texto("Local de atendimento: ")

    lista.inserir(Servico(id_novo, titulo, categoria, descricao, requisitos, local))
    print("Serviço cadastrado com sucesso!")


def listar(lista):
    print("\n--- Serviços cadastrados ---")
    if lista.vazia():
        print("Nenhum serviço cadastrado.")
        return
    mostrar_lista(lista.percorrer())
    print(f"Total: {lista.tamanho}")


def consultar(lista):
    print("\n--- Consultar por ID ---")
    if lista.vazia():
        print("A lista está vazia.")
        return
    id_busca = ler_inteiro("ID: ", 1)
    servico = lista.buscar_por_id(id_busca)
    if servico is None:
        print(f"Nenhum serviço encontrado com o ID {id_busca}.")
    else:
        print(servico)


def pesquisar(lista):
    print("\n--- Pesquisar ---")
    if lista.vazia():
        print("A lista está vazia.")
        return
    print("1 - Título\n2 - Categoria\n3 - Local")
    opcao = ler_inteiro("Pesquisar por: ", 1, 3)
    campo = {1: "titulo", 2: "categoria", 3: "local"}[opcao]
    termo = ler_texto("Termo da pesquisa: ")

    resultado = lista.buscar_por_campo(campo, termo)
    if not resultado:
        print(f"Nenhum serviço encontrado para \"{termo}\".")
        return
    print(f"{len(resultado)} resultado(s):")
    mostrar_lista(resultado)


def atualizar(lista):
    print("\n--- Atualizar serviço ---")
    if lista.vazia():
        print("A lista está vazia.")
        return
    id_busca = ler_inteiro("ID do serviço: ", 1)
    servico = lista.buscar_por_id(id_busca)
    if servico is None:
        print(f"Nenhum serviço encontrado com o ID {id_busca}.")
        return

    print(servico)
    print("\nDeixe em branco para manter o valor atual.")
    novos = {
        "titulo": ler_texto("Novo título: ", False),
        "categoria": escolher_categoria(permitir_manter=True),
        "descricao": ler_texto("Nova descrição: ", False),
        "requisitos": ler_texto("Novos requisitos: ", False),
        "local": ler_texto("Novo local: ", False),
    }
    lista.atualizar(id_busca, novos)
    print("Serviço atualizado.")


def excluir(lista):
    print("\n--- Excluir serviço ---")
    if lista.vazia():
        print("A lista está vazia.")
        return
    id_busca = ler_inteiro("ID do serviço: ", 1)
    servico = lista.buscar_por_id(id_busca)
    if servico is None:
        print(f"Nenhum serviço encontrado com o ID {id_busca}.")
        return

    print(servico.resumo())
    confirma = ler_texto("Confirma a exclusão? (s/n): ").lower()
    if confirma == "s":
        lista.remover(id_busca)
        print("Serviço removido.")
    else:
        print("Exclusão cancelada.")


def ordenar(lista):
    print("\n--- Ordenar ---")
    if lista.vazia():
        print("A lista está vazia.")
        return
    print("1 - ID\n2 - Título\n3 - Categoria")
    opcao = ler_inteiro("Ordenar por: ", 1, 3)
    campo = {1: "id", 2: "titulo", 3: "categoria"}[opcao]
    lista.ordenar(campo)
    print("Lista ordenada (Merge Sort):")
    mostrar_lista(lista.percorrer())


def analise(lista):
    print("\n--- Análise ---")
    if lista.vazia():
        print("Nenhum serviço cadastrado para analisar.")
        return
    total = lista.tamanho
    print(f"Total de serviços: {total}")
    print("Serviços por categoria:")
    contagem = lista.contar_por_categoria()
    for categoria in CATEGORIAS:
        qtd = contagem.get(categoria, 0)
        porcentagem = qtd / total * 100
        print(f"  {categoria:<20} {qtd:>3}  ({porcentagem:.1f}%) {'#' * qtd}")


def carregar_exemplos(lista):
    adicionados = 0
    for servico in gerar_exemplos():
        if lista.inserir(servico):
            adicionados += 1
    print(f"{adicionados} serviço(s) de exemplo adicionados.")
    if adicionados == 0:
        print("Os exemplos já estavam cadastrados.")


MENU = """
===== Citizen Assist AI =====
1 - Cadastrar serviço
2 - Listar serviços
3 - Consultar por ID
4 - Pesquisar
5 - Atualizar serviço
6 - Excluir serviço
7 - Ordenar
8 - Análise
9 - Carregar dados de exemplo
0 - Sair"""


def main():
    lista = ListaEncadeada()
    acoes = {
        1: cadastrar, 2: listar, 3: consultar, 4: pesquisar,
        5: atualizar, 6: excluir, 7: ordenar, 8: analise,
        9: carregar_exemplos,
    }

    while True:
        print(MENU)
        entrada = input("Opção: ").strip()
        if not entrada.isdigit() or int(entrada) not in range(0, 10):
            print("Opção inválida, tente de novo.")
            continue

        opcao = int(entrada)
        if opcao == 0:
            print("Encerrando o sistema. Até mais!")
            break
        acoes[opcao](lista)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")
