import unicodedata


def normalizar(texto):
    # tira acento e deixa minusculo pra comparar "saude" com "Saúde"
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


class No:
    def __init__(self, servico):
        self.servico = servico
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def vazia(self):
        return self.inicio is None

    def inserir(self, servico):
        if self.buscar_por_id(servico.id) is not None:
            return False

        novo = No(servico)
        if self.vazia():
            self.inicio = novo
        else:
            self.fim.proximo = novo
        self.fim = novo
        self.tamanho += 1
        return True

    def percorrer(self):
        atual = self.inicio
        while atual is not None:
            yield atual.servico
            atual = atual.proximo

    def buscar_por_id(self, id_busca):
        atual = self.inicio
        while atual is not None:
            if atual.servico.id == id_busca:
                return atual.servico
            atual = atual.proximo
        return None

    def proximo_id(self):
        maior = 0
        atual = self.inicio
        while atual is not None:
            if atual.servico.id > maior:
                maior = atual.servico.id
            atual = atual.proximo
        return maior + 1

    def buscar_por_campo(self, campo, termo):
        termo = normalizar(termo)
        encontrados = []
        atual = self.inicio
        while atual is not None:
            valor = normalizar(getattr(atual.servico, campo))
            if termo in valor:
                encontrados.append(atual.servico)
            atual = atual.proximo
        return encontrados

    def atualizar(self, id_busca, novos_dados):
        servico = self.buscar_por_id(id_busca)
        if servico is None:
            return False
        for campo, valor in novos_dados.items():
            if valor:
                setattr(servico, campo, valor)
        return True

    def remover(self, id_remover):
        anterior = None
        atual = self.inicio
        while atual is not None and atual.servico.id != id_remover:
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return None

        if anterior is None:
            self.inicio = atual.proximo
        else:
            anterior.proximo = atual.proximo

        if atual is self.fim:
            self.fim = anterior

        self.tamanho -= 1
        return atual.servico

    def ordenar(self, campo):
        self.inicio = self._merge_sort(self.inicio, campo)

        # depois de ordenar o fim muda, entao acha de novo
        atual = self.inicio
        while atual is not None and atual.proximo is not None:
            atual = atual.proximo
        self.fim = atual

    def _chave(self, no, campo):
        valor = getattr(no.servico, campo)
        if isinstance(valor, str):
            return normalizar(valor)
        return valor

    def _merge_sort(self, cabeca, campo):
        if cabeca is None or cabeca.proximo is None:
            return cabeca

        meio = self._dividir(cabeca)
        esquerda = self._merge_sort(cabeca, campo)
        direita = self._merge_sort(meio, campo)
        return self._intercalar(esquerda, direita, campo)

    def _dividir(self, cabeca):
        lento = cabeca
        rapido = cabeca.proximo
        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo

        meio = lento.proximo
        lento.proximo = None
        return meio

    def _intercalar(self, a, b, campo):
        auxiliar = No(None)
        cauda = auxiliar

        while a is not None and b is not None:
            if self._chave(a, campo) <= self._chave(b, campo):
                cauda.proximo = a
                a = a.proximo
            else:
                cauda.proximo = b
                b = b.proximo
            cauda = cauda.proximo

        cauda.proximo = a if a is not None else b
        return auxiliar.proximo

    def contar_por_categoria(self):
        contagem = {}
        for servico in self.percorrer():
            contagem[servico.categoria] = contagem.get(servico.categoria, 0) + 1
        return contagem
