import pandas as pd
import streamlit as st

from servico import Servico, CATEGORIAS
from lista import ListaEncadeada
from dados_exemplo import gerar_exemplos

st.set_page_config(page_title="Citizen Assist AI")

# o streamlit roda o script de novo a cada clique, entao a lista fica na sessao
if "lista" not in st.session_state:
    st.session_state.lista = ListaEncadeada()

lista = st.session_state.lista


def tabela(servicos):
    linhas = [
        {"ID": s.id, "Título": s.titulo, "Categoria": s.categoria, "Local": s.local}
        for s in servicos
    ]
    st.table(pd.DataFrame(linhas), hide_index=True)


def detalhes(servico):
    st.markdown(
        f"**ID:** {servico.id}  \n"
        f"**Título:** {servico.titulo}  \n"
        f"**Categoria:** {servico.categoria}  \n"
        f"**Descrição:** {servico.descricao}  \n"
        f"**Requisitos:** {servico.requisitos}  \n"
        f"**Local:** {servico.local}"
    )


def campos_vazios(*campos):
    return any(not c.strip() for c in campos)


CAMPOS_CADASTRO = ["cad_titulo", "cad_descricao", "cad_requisitos", "cad_local"]


def tela_cadastrar():
    st.header("Cadastrar serviço")

    # depois de cadastrar limpa o form e ja sugere o proximo id
    if st.session_state.pop("limpar_cadastro", False):
        for chave in CAMPOS_CADASTRO:
            st.session_state[chave] = ""
        st.session_state.cad_id = lista.proximo_id()
    if "cad_id" not in st.session_state:
        st.session_state.cad_id = lista.proximo_id()
    if "msg_cadastro" in st.session_state:
        st.success(st.session_state.pop("msg_cadastro"))

    with st.form("form_cadastro"):
        id_novo = st.number_input("ID", min_value=1, step=1, key="cad_id",
                                  help="Já vem com o próximo ID livre, mas pode ser alterado.")
        titulo = st.text_input("Título", key="cad_titulo")
        categoria = st.selectbox("Categoria", CATEGORIAS)
        descricao = st.text_area("Descrição", key="cad_descricao")
        requisitos = st.text_input("Requisitos", key="cad_requisitos")
        local = st.text_input("Local de atendimento", key="cad_local")
        enviado = st.form_submit_button("Cadastrar")

    if not enviado:
        return
    if campos_vazios(titulo, descricao, requisitos, local):
        st.error("Preencha todos os campos.")
        return

    novo = Servico(int(id_novo), titulo.strip(), categoria, descricao.strip(),
                   requisitos.strip(), local.strip())
    if lista.inserir(novo):
        st.session_state.msg_cadastro = f"Serviço {id_novo} cadastrado com sucesso!"
        st.session_state.limpar_cadastro = True
        st.rerun()
    else:
        st.error(f"Já existe um serviço com o ID {id_novo}.")


def tela_listar():
    st.header("Serviços cadastrados")
    tabela(lista.percorrer())
    st.caption(f"Total: {lista.tamanho}")


def tela_consultar():
    st.header("Consultar por ID")
    id_busca = st.number_input("ID", min_value=1, step=1, value=None,
                               placeholder="Digite o ID", key="id_consulta")
    if st.button("Buscar"):
        if id_busca is None:
            st.error("Digite um ID para buscar.")
            return
        id_busca = int(id_busca)
        servico = lista.buscar_por_id(id_busca)
        if servico is None:
            st.warning(f"Nenhum serviço encontrado com o ID {id_busca}.")
        else:
            detalhes(servico)


def tela_pesquisar():
    st.header("Pesquisar")
    opcoes = {"Título": "titulo", "Categoria": "categoria", "Local": "local"}
    campo = st.selectbox("Pesquisar por", list(opcoes))
    termo = st.text_input("Termo da pesquisa")

    if st.button("Pesquisar"):
        if not termo.strip():
            st.error("Digite um termo para pesquisar.")
            return
        resultado = lista.buscar_por_campo(opcoes[campo], termo.strip())
        if not resultado:
            st.warning(f"Nenhum serviço encontrado para \"{termo}\".")
        else:
            st.write(f"{len(resultado)} resultado(s):")
            tabela(resultado)


def tela_atualizar():
    st.header("Atualizar serviço")
    id_busca = st.number_input("ID do serviço", min_value=1, step=1, value=None,
                               placeholder="Digite o ID", key="id_atualizar")
    if id_busca is None:
        return
    id_busca = int(id_busca)
    servico = lista.buscar_por_id(id_busca)
    if servico is None:
        st.warning(f"Nenhum serviço encontrado com o ID {id_busca}.")
        return

    # a key muda com o id pra recarregar os valores quando troca de servico
    with st.form(f"form_atualizar_{id_busca}"):
        titulo = st.text_input("Título", servico.titulo)
        categoria = st.selectbox("Categoria", CATEGORIAS,
                                 index=CATEGORIAS.index(servico.categoria))
        descricao = st.text_area("Descrição", servico.descricao)
        requisitos = st.text_input("Requisitos", servico.requisitos)
        local = st.text_input("Local de atendimento", servico.local)
        enviado = st.form_submit_button("Salvar alterações")

    if not enviado:
        return
    if campos_vazios(titulo, descricao, requisitos, local):
        st.error("Nenhum campo pode ficar vazio.")
        return

    lista.atualizar(id_busca, {
        "titulo": titulo.strip(),
        "categoria": categoria,
        "descricao": descricao.strip(),
        "requisitos": requisitos.strip(),
        "local": local.strip(),
    })
    st.success("Serviço atualizado.")


def tela_excluir():
    st.header("Excluir serviço")
    id_busca = st.number_input("ID do serviço", min_value=1, step=1, value=None,
                               placeholder="Digite o ID", key="id_excluir")
    if id_busca is None:
        return
    id_busca = int(id_busca)
    servico = lista.buscar_por_id(id_busca)
    if servico is None:
        st.warning(f"Nenhum serviço encontrado com o ID {id_busca}.")
        return

    st.write(servico.resumo())
    confirma = st.checkbox("Confirmo que quero excluir este serviço")
    if st.button("Excluir"):
        if not confirma:
            st.error("Marque a confirmação antes de excluir.")
        else:
            lista.remover(id_busca)
            st.success(f"Serviço {id_busca} removido.")


def tela_ordenar():
    st.header("Ordenar")
    opcoes = {"ID": "id", "Título": "titulo", "Categoria": "categoria"}
    campo = st.selectbox("Ordenar por", list(opcoes))
    if st.button("Ordenar"):
        lista.ordenar(opcoes[campo])
        st.success(f"Lista ordenada por {campo} (Merge Sort).")
    tabela(lista.percorrer())


def tela_analise():
    st.header("Análise")
    total = lista.tamanho
    contagem = lista.contar_por_categoria()

    st.metric("Total de serviços", total)
    linhas = []
    for categoria in CATEGORIAS:
        qtd = contagem.get(categoria, 0)
        linhas.append({
            "Categoria": categoria,
            "Quantidade": qtd,
            "Porcentagem": f"{qtd / total * 100:.1f}%",
        })
    dados = pd.DataFrame(linhas).set_index("Categoria")
    st.table(dados)
    st.bar_chart(dados["Quantidade"], sort=False)


TELAS = {
    "Cadastrar": tela_cadastrar,
    "Listar": tela_listar,
    "Consultar por ID": tela_consultar,
    "Pesquisar": tela_pesquisar,
    "Atualizar": tela_atualizar,
    "Excluir": tela_excluir,
    "Ordenar": tela_ordenar,
    "Análise": tela_analise,
}

def ir_para(tela):
    st.session_state.tela = tela
    st.rerun()


def tela_boas_vindas():
    st.title("Citizen Assist AI")
    st.subheader("Seja bem-vindo ao nosso app Citizen Assist AI, deseja iniciar?")
    st.write("Aqui você encontra serviços e orientações ao cidadão: saúde, "
             "documentação, assistência social, educação e serviços urbanos.")
    if st.button("Iniciar", type="primary"):
        ir_para("app")


def tela_encerramento():
    st.title("Obrigado por usar nossa aplicação!")
    st.write(f"Serviços cadastrados nesta sessão: {lista.tamanho}")
    if st.button("Fazer mais registros", type="primary"):
        st.session_state.menu = "Cadastrar"
        ir_para("app")


def tela_principal():
    st.sidebar.title("Citizen Assist AI")
    escolha = st.sidebar.radio("Menu", list(TELAS), key="menu")

    if st.sidebar.button("Carregar dados de exemplo"):
        adicionados = sum(1 for s in gerar_exemplos() if lista.inserir(s))
        st.session_state.pop("cad_id", None)
        if adicionados:
            st.sidebar.success(f"{adicionados} serviço(s) adicionados.")
        else:
            st.sidebar.info("Os exemplos já estavam cadastrados.")

    if escolha != "Cadastrar" and lista.vazia():
        st.header(escolha)
        st.info("Nenhum serviço cadastrado. Cadastre um serviço ou carregue os dados de exemplo.")
    else:
        TELAS[escolha]()

    st.sidebar.caption(f"Serviços na lista: {lista.tamanho}")
    st.sidebar.divider()
    if st.sidebar.button("Encerrar"):
        ir_para("fim")


if "tela" not in st.session_state:
    st.session_state.tela = "inicio"

if st.session_state.tela == "inicio":
    tela_boas_vindas()
elif st.session_state.tela == "fim":
    tela_encerramento()
else:
    tela_principal()
