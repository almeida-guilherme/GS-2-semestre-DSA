import unittest
from unittest.mock import patch

from servico import Servico
from lista import ListaEncadeada
from dados_exemplo import gerar_exemplos
from main import ler_inteiro, ler_texto


def criar(id, titulo="Teste", categoria="Saúde"):
    return Servico(id, titulo, categoria, "desc", "req", "local")


class TestListaVazia(unittest.TestCase):
    def setUp(self):
        self.lista = ListaEncadeada()

    def test_lista_comeca_vazia(self):
        self.assertTrue(self.lista.vazia())
        self.assertEqual(self.lista.tamanho, 0)

    def test_buscar_em_lista_vazia(self):
        self.assertIsNone(self.lista.buscar_por_id(1))
        self.assertEqual(self.lista.buscar_por_campo("titulo", "rg"), [])

    def test_remover_em_lista_vazia(self):
        self.assertIsNone(self.lista.remover(1))

    def test_ordenar_lista_vazia(self):
        self.lista.ordenar("titulo")
        self.assertIsNone(self.lista.inicio)
        self.assertIsNone(self.lista.fim)

    def test_analise_lista_vazia(self):
        self.assertEqual(self.lista.contar_por_categoria(), {})


class TestOperacoes(unittest.TestCase):
    def setUp(self):
        self.lista = ListaEncadeada()
        for servico in gerar_exemplos():
            self.lista.inserir(servico)

    def test_inserir(self):
        self.assertEqual(self.lista.tamanho, 8)
        self.assertTrue(self.lista.inserir(criar(200)))
        self.assertEqual(self.lista.fim.servico.id, 200)

    def test_id_duplicado(self):
        self.assertFalse(self.lista.inserir(criar(101)))
        self.assertEqual(self.lista.tamanho, 8)

    def test_buscar_por_id(self):
        self.assertEqual(self.lista.buscar_por_id(103).titulo, "Cadastro no CadÚnico")

    def test_buscar_id_inexistente(self):
        self.assertIsNone(self.lista.buscar_por_id(999))

    def test_pesquisa_sem_acento(self):
        resultado = self.lista.buscar_por_campo("categoria", "saude")
        self.assertEqual([s.id for s in resultado], [102, 106])

    def test_pesquisa_parcial_titulo(self):
        resultado = self.lista.buscar_por_campo("titulo", "carteira")
        self.assertEqual(len(resultado), 1)

    def test_pesquisa_sem_resultado(self):
        self.assertEqual(self.lista.buscar_por_campo("titulo", "passaporte"), [])

    def test_atualizar(self):
        self.assertTrue(self.lista.atualizar(101, {"titulo": "RG novo", "local": ""}))
        servico = self.lista.buscar_por_id(101)
        self.assertEqual(servico.titulo, "RG novo")
        self.assertEqual(servico.local, "Poupatempo Sé")

    def test_atualizar_inexistente(self):
        self.assertFalse(self.lista.atualizar(999, {"titulo": "x"}))

    def test_remover_inicio_meio_fim(self):
        self.lista.remover(101)
        self.assertEqual(self.lista.inicio.servico.id, 102)
        self.lista.remover(104)
        self.lista.remover(108)
        self.assertEqual(self.lista.fim.servico.id, 107)
        self.assertEqual([s.id for s in self.lista.percorrer()], [102, 103, 105, 106, 107])
        self.assertEqual(self.lista.tamanho, 5)

    def test_remover_inexistente(self):
        self.assertIsNone(self.lista.remover(999))
        self.assertEqual(self.lista.tamanho, 8)

    def test_remover_unico_elemento(self):
        lista = ListaEncadeada()
        lista.inserir(criar(1))
        lista.remover(1)
        self.assertTrue(lista.vazia())
        self.assertIsNone(lista.fim)
        lista.inserir(criar(2))
        self.assertEqual(lista.inicio.servico.id, 2)

    def test_ordenar_por_titulo(self):
        self.lista.ordenar("titulo")
        titulos = [s.titulo for s in self.lista.percorrer()]
        self.assertEqual(titulos[0], "Bolsa Família")
        self.assertEqual(titulos[-1], "Vacinação contra gripe")
        self.assertEqual(self.lista.fim.servico.titulo, "Vacinação contra gripe")

    def test_ordenar_por_id(self):
        lista = ListaEncadeada()
        for i in [5, 3, 9, 1, 7]:
            lista.inserir(criar(i))
        lista.ordenar("id")
        self.assertEqual([s.id for s in lista.percorrer()], [1, 3, 5, 7, 9])

    def test_ordenacao_estavel(self):
        self.lista.ordenar("categoria")
        saude = [s.id for s in self.lista.percorrer() if s.categoria == "Saúde"]
        self.assertEqual(saude, [102, 106])

    def test_inserir_depois_de_ordenar(self):
        self.lista.ordenar("titulo")
        self.lista.inserir(criar(300))
        self.assertEqual(self.lista.fim.servico.id, 300)

    def test_proximo_id(self):
        self.assertEqual(ListaEncadeada().proximo_id(), 1)
        self.assertEqual(self.lista.proximo_id(), 109)
        self.lista.inserir(criar(500))
        self.assertEqual(self.lista.proximo_id(), 501)

    def test_contar_por_categoria(self):
        contagem = self.lista.contar_por_categoria()
        self.assertEqual(contagem["Saúde"], 2)
        self.assertEqual(contagem["Educação"], 1)
        self.assertEqual(sum(contagem.values()), 8)


class TestEntradas(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["abc", "", "-3", "5"])
    def test_ler_inteiro_invalido(self, mock_input, mock_print):
        self.assertEqual(ler_inteiro("ID: ", 1), 5)
        self.assertEqual(mock_input.call_count, 4)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["10", "3"])
    def test_ler_inteiro_fora_do_limite(self, mock_input, mock_print):
        self.assertEqual(ler_inteiro("Opção: ", 1, 5), 3)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["   ", "Emissão de CPF"])
    def test_ler_texto_vazio(self, mock_input, mock_print):
        self.assertEqual(ler_texto("Título: "), "Emissão de CPF")

    @patch("builtins.input", return_value="")
    def test_ler_texto_opcional(self, mock_input):
        self.assertEqual(ler_texto("Novo título: ", False), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
