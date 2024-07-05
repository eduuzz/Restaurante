#Leonardo Taborda, Eduardo Santos e Eduardo Dalpra

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QMessageBox, QDialog, QSpinBox, QLabel
from PySide6.QtCore import Qt
from qdarktheme import load_stylesheet
from classes import ItemDoCardapio, Pedido, Restaurante

class MainWindow(QMainWindow):
    def __init__(self, restaurante):
        super().__init__()
        self.restaurante = restaurante

        self.setWindowTitle("Gerenciamento de Pedidos")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.pedidos_list = QListWidget()
        layout.addWidget(self.pedidos_list)

        self.preparacao_list = QListWidget()
        layout.addWidget(self.preparacao_list)

        self.entregue_list = QListWidget()
        layout.addWidget(self.entregue_list)

        botao_novo_pedido = QPushButton("Novo Pedido")
        botao_novo_pedido.clicked.connect(self.novo_pedido)
        layout.addWidget(botao_novo_pedido)

        botao_preparar = QPushButton("Preparar Pedido")
        botao_preparar.clicked.connect(self.preparar_pedido)
        layout.addWidget(botao_preparar)

        botao_entregar = QPushButton("Entregar Pedido")
        botao_entregar.clicked.connect(self.entregar_pedido)
        layout.addWidget(botao_entregar)

        botao_relatorio = QPushButton("Relatório")
        botao_relatorio.clicked.connect(self.gerar_relatorio)
        layout.addWidget(botao_relatorio)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.atualizar_listas()

    def novo_pedido(self):
        dialog = NovoPedidoDialog(self.restaurante, self)
        if dialog.exec():
            pedido = dialog.obter_pedido()
            self.restaurante.adicionar_pedido(pedido)
            self.atualizar_listas()

    def preparar_pedido(self):
        item_selecionado = self.pedidos_list.currentItem()
        if item_selecionado:
            pedido = item_selecionado.data(Qt.UserRole)
            self.restaurante.mudar_status_pedido(pedido, 'Em preparação')
            self.atualizar_listas()

    def entregar_pedido(self):
        item_selecionado = self.preparacao_list.currentItem()
        if item_selecionado:
            pedido = item_selecionado.data(Qt.UserRole)
            self.restaurante.mudar_status_pedido(pedido, 'Entregue')
            self.atualizar_listas()

    def gerar_relatorio(self):
        total, itens_vendidos = self.restaurante.relatorio_faturamento()
        mensagem = f"Faturamento total: R${total:.2f}\n"
        mensagem += "Itens vendidos:\n"
        for item, quantidade in itens_vendidos.items():
            mensagem += f"{item}: {quantidade}\n"
        QMessageBox.information(self, "Relatório", mensagem)

    def atualizar_listas(self):
        self.pedidos_list.clear()
        for pedido in self.restaurante.filas_pedidos['Pedido']:
            item = QListWidgetItem(str(pedido))
            item.setData(Qt.UserRole, pedido)
            self.pedidos_list.addItem(item)

        self.preparacao_list.clear()
        for pedido in self.restaurante.filas_pedidos['Em preparação']:
            item = QListWidgetItem(str(pedido))
            item.setData(Qt.UserRole, pedido)
            self.preparacao_list.addItem(item)

        self.entregue_list.clear()
        for pedido in self.restaurante.filas_pedidos['Entregue']:
            item = QListWidgetItem(str(pedido))
            item.setData(Qt.UserRole, pedido)
            self.entregue_list.addItem(item)

class NovoPedidoDialog(QDialog):
    def __init__(self, restaurante, parent=None):
        super().__init__(parent)
        self.restaurante = restaurante
        self.setWindowTitle("Novo Pedido")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.numero_mesa_edit = QLineEdit()
        form_layout.addRow("Número da Mesa:", self.numero_mesa_edit)
        layout.addLayout(form_layout)

        self.itens_list = QListWidget()
        for item in self.restaurante.cardapio:
            list_item = QListWidgetItem(str(item))
            list_item.setData(Qt.UserRole, item)
            self.itens_list.addItem(list_item)
        layout.addWidget(self.itens_list)

        self.quantidade_spin = QSpinBox()
        self.quantidade_spin.setRange(1, 100)
        layout.addWidget(QLabel("Quantidade:"))
        layout.addWidget(self.quantidade_spin)

        botao_adicionar = QPushButton("Adicionar Item")
        botao_adicionar.clicked.connect(self.adicionar_item)
        layout.addWidget(botao_adicionar)

        self.pedido_itens_list = QListWidget()
        layout.addWidget(self.pedido_itens_list)

        botao_finalizar_pedido = QPushButton("Finalizar Pedido")
        botao_finalizar_pedido.clicked.connect(self.accept)
        layout.addWidget(botao_finalizar_pedido)

        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)

        self.pedido_itens = []

    def adicionar_item(self):
        item_selecionado = self.itens_list.currentItem()
        quantidade = self.quantidade_spin.value()
        if item_selecionado and quantidade > 0:
            item = item_selecionado.data(Qt.UserRole)
            self.pedido_itens.append((item, quantidade))
            self.pedido_itens_list.addItem(f"{item.nome} x{quantidade}")

    def obter_pedido(self):
        numero_pedido = len(self.restaurante.filas_pedidos['Pedido']) + len(self.restaurante.filas_pedidos['Em preparação']) + len(self.restaurante.filas_pedidos['Entregue']) + 1
        numero_mesa = int(self.numero_mesa_edit.text())
        pedido = Pedido(numero_pedido, numero_mesa)
        for item, quantidade in self.pedido_itens:
            pedido.adicionar_item(item, quantidade)
        return pedido

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    restaurante = Restaurante()
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Hambúrguer", 25.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Hambúrguer Vegano", 25.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Pizza Grande", 55.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Pizza Média", 45.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Pizza Doce (Pequena)", 38.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Suco de laranja", 3.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Água 500ml", 2.00))
    restaurante.adicionar_item_cardapio(ItemDoCardapio("Coca-Cola 2l", 6.00))

    window = MainWindow(restaurante)
    window.show()

    sys.exit(app.exec())
