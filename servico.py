CATEGORIAS = [
    "Saúde",
    "Assistência social",
    "Documentação",
    "Educação",
    "Serviços urbanos",
]


class Servico:
    def __init__(self, id, titulo, categoria, descricao, requisitos, local):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.requisitos = requisitos
        self.local = local

    def resumo(self):
        return f"[{self.id}] {self.titulo} ({self.categoria})"

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Categoria: {self.categoria}\n"
            f"Descrição: {self.descricao}\n"
            f"Requisitos: {self.requisitos}\n"
            f"Local: {self.local}"
        )
