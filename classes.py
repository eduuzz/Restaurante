#Leonardo Taborda, Eduardo Santos e Eduardo Dalpra

class ItemDoCardapio:
    def __init__(self, nome, preco, descricao=""):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao

    def __repr__(self):
        return f"{self.nome} - R${self.preco:.2f}"

class Pedido:
    def __init__(self, numero_pedido, numero_mesa):
        self.numero_pedido = numero_pedido
        self.numero_mesa = numero_mesa
        self.itens = []
        self.status = 'Pedido'

    def adicionar_item(self, item, quantidade):
        self.itens.append((item, quantidade))

    def calcular_total(self):
        return sum(item.preco * quantidade for item, quantidade in self.itens)

    def __repr__(self):
        itens_str = ', '.join([f"{item.nome} x{quantidade}" for item, quantidade in self.itens])
        return f"Pedido #{self.numero_pedido} - Mesa #{self.numero_mesa} - Itens: {itens_str} - Status: {self.status}"

from collections import deque

class Restaurante:
    def __init__(self):
        self.cardapio = []
        self.filas_pedidos = {
            'Pedido': deque(),
            'Em preparação': deque(),
            'Entregue': deque()
        }
        self.pedidos_entregues = []

    def adicionar_item_cardapio(self, item):
        self.cardapio.append(item)

    def adicionar_pedido(self, pedido):
        self.filas_pedidos['Pedido'].append(pedido)

    def mudar_status_pedido(self, pedido, novo_status):
        self.filas_pedidos[pedido.status].remove(pedido)
        pedido.status = novo_status
        self.filas_pedidos[novo_status].append(pedido)
        if novo_status == 'Entregue':
            self.pedidos_entregues.append(pedido)

    def relatorio_faturamento(self):
        total = 0
        itens_vendidos = {}
        for pedido in self.pedidos_entregues:
            total += pedido.calcular_total()
            for item, quantidade in pedido.itens:
                if item.nome in itens_vendidos:
                    itens_vendidos[item.nome] += quantidade
                else:
                    itens_vendidos[item.nome] = quantidade
        return total, itens_vendidos
