# Citizen Assist AI - DSA

Global Solution 2026.2 (Citizen Tech) - Data Structures and Algorithms.

**App publicado:** https://citizen-assist-dsa.streamlit.app/

Sistema em Python, rodando no terminal, para cadastrar e consultar serviços e orientações ao cidadão. Os dados ficam numa lista encadeada feita por nós, e a busca e a ordenação também são implementação própria.

## Como executar

Precisa de Python 3.8 ou mais novo. Não usa nenhuma biblioteca externa.

```bash
python3 main.py
```

Para rodar os testes:

```bash
python3 -m unittest -v test_sistema
```

### Interface web (opcional)

Além do menu no terminal, fizemos uma interface em Streamlit (`app.py`). Ela usa a mesma `ListaEncadeada`, a mesma busca e o mesmo Merge Sort; só a tela muda.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Também está publicada no Streamlit Community Cloud: https://citizen-assist-dsa.streamlit.app/

Rodando local, abre no navegador em `http://localhost:8501`, numa tela de boas-vindas com o botão "Iniciar". O menu fica na barra lateral, junto com o botão para carregar os dados de exemplo e o botão "Encerrar". Encerrar leva para uma tela de agradecimento, que tem o botão "Fazer mais registros" para voltar ao cadastro. Como o Streamlit executa o script de novo a cada clique, a lista fica guardada em `st.session_state`. Os dados duram enquanto a aba estiver aberta.

No cadastro, o campo ID já vem com o próximo ID livre (maior ID + 1, pelo método `proximo_id()`). Ele continua editável, então um ID repetido ainda é recusado com mensagem de erro.

As tabelas usam `st.table`, que não deixa ordenar clicando na coluna. Assim toda ordenação que aparece na tela vem do nosso Merge Sort.

## Recorte escolhido

Escolhemos um catálogo geral de serviços públicos, dividido em 5 categorias fixas:
Saúde, Assistência social, Documentação, Educação e Serviços urbanos.

A ideia é o cidadão conseguir achar rápido um serviço (ex.: "como tiro o RG?"), ver o que precisa levar e onde ir. A opção 9 do menu carrega 8 serviços de exemplo para facilitar a demonstração.

## Arquivos

| Arquivo | O que tem |
|---|---|
| `servico.py` | Classe `Servico` (o registro) e a lista de categorias |
| `lista.py` | Classes `No` e `ListaEncadeada`, com busca, remoção e Merge Sort |
| `main.py` | Menu, leitura e validação das entradas |
| `app.py` | Interface web em Streamlit (opcional) |
| `requirements.txt` | Dependência da interface web |
| `dados_exemplo.py` | Serviços de exemplo |
| `test_sistema.py` | Testes automatizados (unittest) |
| `evidencias/` | Saída dos testes e de uma execução do menu |

## Modelo do registro

| Campo | Tipo | Observação |
|---|---|---|
| `id` | int | Único, maior que zero, digitado pelo usuário |
| `titulo` | str | Obrigatório |
| `categoria` | str | Escolhida numa lista fixa de 5 categorias |
| `descricao` | str | Obrigatório |
| `requisitos` | str | Documentos ou condições necessárias |
| `local` | str | Onde o cidadão é atendido |

## Estrutura da lista encadeada

Cada `No` guarda um `Servico` e a referência para o próximo nó (`proximo`).
A `ListaEncadeada` guarda:

- `inicio`: primeiro nó
- `fim`: último nó, para inserir no final sem percorrer tudo
- `tamanho`: quantidade de nós

```
inicio                                          fim
  |                                              |
[101 | o]--> [102 | o]--> [103 | o]--> ... --> [108 | None]
```

Operações:

- **inserir**: verifica se o ID já existe; se não existir, liga o novo nó depois do `fim`.
- **percorrer**: anda de nó em nó a partir do `inicio` até chegar em `None`.
- **remover**: procura o nó guardando o anterior. Depois liga o anterior direto no próximo. Trata os casos de remover o primeiro, o último e o único elemento (atualizando `inicio` e `fim`).
- **atualizar**: acha o registro pelo ID e troca só os campos que foram preenchidos.

## Algoritmo de busca

Usamos **busca linear (sequencial)**, porque numa lista encadeada não dá para acessar o meio direto, então não tem como fazer busca binária.

- **Por ID** (`buscar_por_id`): começa no `inicio` e compara o ID de cada nó. Para no primeiro que bater. Se chegar no fim da lista sem achar, retorna `None` e o menu mostra "Nenhum serviço encontrado com o ID X".
- **Por atributo** (`buscar_por_campo`): pesquisa por título, categoria ou local. Percorre a lista inteira e junta todos os que contêm o termo digitado (busca parcial). Antes de comparar, os dois textos passam por `normalizar()`, que tira acentos e deixa tudo minúsculo, assim "saude" encontra "Saúde". Se nada for encontrado, retorna uma lista vazia e o menu avisa o usuário.

## Algoritmo de ordenação

Usamos **Merge Sort** direto nos nós da lista (não copiamos para uma lista do Python e não usamos `sort()`/`sorted()`).

1. **Dividir**: acha o meio da lista com dois ponteiros, um anda de 1 em 1 (`lento`) e outro de 2 em 2 (`rapido`). Quando o rápido chega no fim, o lento está no meio, e a lista é cortada ali.
2. **Ordenar** cada metade recursivamente, até sobrar listas de 1 nó.
3. **Intercalar**: junta as duas metades já ordenadas, sempre pegando o menor dos dois primeiros nós.

Dá para ordenar por ID, título ou categoria. Os textos são comparados sem acento e sem diferenciar maiúscula. Como usamos `<=` na intercalação, a ordenação é estável (serviços da mesma categoria mantêm a ordem que já tinham). No final o ponteiro `fim` é atualizado.

Escolhemos Merge Sort porque ele funciona bem em lista encadeada: não precisa de acesso por índice e reaproveita os próprios nós, só mudando os ponteiros.

## Análise de complexidade (Big-O)

n = número de serviços cadastrados.

| Operação | Tempo | Justificativa |
|---|---|---|
| Inserção (só ligar o nó) | O(1) | Usamos o ponteiro `fim`, então não precisa percorrer |
| Inserção com checagem de ID | O(n) | Antes de inserir, buscamos o ID para não deixar duplicado |
| Busca por ID | O(n) | Pior caso: o ID está no fim ou não existe. Melhor caso O(1), se for o primeiro |
| Busca por atributo | O(n · m) | Sempre percorre a lista toda; m é o tamanho do texto comparado |
| Atualização | O(n) | Custo de achar o registro; trocar os campos é O(1) |
| Remoção | O(n) | Precisa achar o nó e o anterior; a religação é O(1) |
| Percurso / listagem | O(n) | Passa uma vez por cada nó |
| Ordenação (Merge Sort) | O(n log n) | A lista é dividida ao meio log n vezes e cada nível intercala n nós. Vale para melhor, médio e pior caso |
| Análise por categoria | O(n) | Uma passada contando num dicionário |
| Próximo ID livre | O(n) | Percorre a lista procurando o maior ID |

Memória: a lista usa O(n). O Merge Sort não cria nós novos, só usa a pilha da recursão, que tem profundidade O(log n).

## Menu

```
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
0 - Sair
```

Validações feitas:

- Opção do menu que não é número ou não existe: mostra "Opção inválida" e volta pro menu.
- ID ou opção com letras, vazio, negativo ou fora do intervalo: pede de novo.
- Campo de texto obrigatório vazio: pede de novo.
- ID duplicado no cadastro: cancela e avisa.
- Consultar, pesquisar, atualizar, excluir, ordenar ou analisar com a lista vazia: avisa que está vazia.
- ID inexistente ou pesquisa sem resultado: avisa que nada foi encontrado.
- Exclusão pede confirmação (s/n).
- Ctrl+C ou fim da entrada encerram o programa sem erro.

## Testes

São 27 testes automatizados em `test_sistema.py`. Saída completa em `evidencias/resultado_testes.txt`.

| Caso | Entrada | Esperado | Obtido |
|---|---|---|---|
| Lista nova | - | vazia, tamanho 0 | OK |
| Buscar em lista vazia | ID 1, título "rg" | `None` e `[]` | OK |
| Remover em lista vazia | ID 1 | `None`, sem erro | OK |
| Ordenar lista vazia | campo título | `inicio` e `fim` continuam `None` | OK |
| Análise com lista vazia | - | dicionário vazio | OK |
| Inserir | ID 200 | tamanho 9, vira o `fim` | OK |
| ID duplicado | ID 101 já existente | recusa, tamanho continua 8 | OK |
| Buscar ID existente | 103 | "Cadastro no CadÚnico" | OK |
| Buscar ID inexistente | 999 | `None` | OK |
| Pesquisa sem acento | categoria "saude" | IDs 102 e 106 | OK |
| Pesquisa parcial | título "carteira" | 1 resultado | OK |
| Pesquisa sem resultado | título "passaporte" | `[]` | OK |
| Atualizar | ID 101, novo título, local vazio | título muda, local mantém | OK |
| Atualizar inexistente | ID 999 | `False` | OK |
| Remover início, meio e fim | 101, 104, 108 | ordem 102,103,105,106,107; `inicio` e `fim` corretos | OK |
| Remover inexistente | 999 | `None`, tamanho 8 | OK |
| Remover único elemento | lista com 1 nó | lista vazia e `fim` = `None` | OK |
| Ordenar por título | exemplos | começa em "Bolsa Família", termina em "Vacinação contra gripe" | OK |
| Ordenar por ID | 5,3,9,1,7 | 1,3,5,7,9 | OK |
| Estabilidade | ordenar por categoria | Saúde continua 102 antes de 106 | OK |
| Inserir após ordenar | ID 300 | entra no fim certo | OK |
| Contagem por categoria | exemplos | Saúde 2, Educação 1, total 8 | OK |
| Próximo ID livre | lista vazia, exemplos, depois ID 500 | 1, 109 e 501 | OK |
| Inteiro inválido | "abc", "", "-3", "5" | rejeita 3 e aceita 5 | OK |
| Inteiro fora do limite | "10" (máx 5), "3" | aceita 3 | OK |
| Texto obrigatório vazio | "   ", "Emissão de CPF" | aceita o segundo | OK |
| Texto opcional vazio | "" | retorna "" | OK |

### Execução pelo menu

O arquivo `evidencias/execucao_menu.txt` tem a saída de uma execução real do programa, com esta sequência:

1. Listar, consultar e analisar com a lista vazia: avisos de lista vazia.
2. Opções inválidas "abc" e "15": "Opção inválida".
3. Carregar exemplos e listar: 8 serviços.
4. Cadastrar com ID 101: recusado por duplicidade.
5. Cadastrar ID 200 deixando o título vazio na primeira tentativa: pede de novo e cadastra.
6. Consultar 200 (encontrado) e 999 (não encontrado).
7. Pesquisar categoria "saude" (2 resultados) e título "passaporte" (nenhum).
8. Ordenar por título com Merge Sort.
9. Atualizar o local do 104 e consultar de novo para conferir.
10. Excluir o 105 (confirmado) e tentar excluir o 999 (não existe).
11. Análise por categoria e sair.

## Integrantes

- André Santos de Azevedo - RM572236
- Guilherme Henrique de Almeida - RM568708
- Renan de Castro Albuquerque - RM570532

## Link da demonstração

https://youtu.be/V_nqdLl-3GM
