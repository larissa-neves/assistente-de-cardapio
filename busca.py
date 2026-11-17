import json
from dataclasses import dataclass, field

@dataclass
class Prato:
    restaurante: str
    nome: str
    preco: float
    tags: list[str] = field(default_factory=list)

def carregar_pratos(caminho):
    with open(caminho, encoding='UTF-8') as arquivo:
        restaurantes = json.load(arquivo)
    pratos = []
    for restaurante in restaurantes: 
        for item in restaurante["pratos"]:
            pratos.append(Prato(restaurante=restaurante["restaurante"], nome=item["nome"],
                                preco=item["preco"], tags=item["tags"]))
    return pratos   

    