from PySide6.QtWidgets import \
    QMainWindow, QVBoxLayout, QComboBox, \
    QLabel, QLineEdit, QWidget, \
    QPushButton, QMessageBox, QSizePolicy, QTableWidget, QAbstractItemView, \
    QApplication, QTableWidgetItem, QTextEdit

from model.nota import Nota
from controller.nota_dao import Database
import requests
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bloco de Notas')
        self.setMinimumSize(500, 900)

        self.lbl_id = QLabel('Bloco de Notas')
        self.lbl_titulo = QLabel('Titulo', self)
        self.txt_titulo = QLineEdit(self)
        self.lbl_nota = QLabel('Nota', self)
        self.txt_nota = QTextEdit(self)

        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.tabela_notas = QTableWidget()

        self.tabela_notas.setColumnCount(4)
        self.tabela_notas.setHorizontalHeaderLabels(['ID', 'Título', 'Nota', 'Data Da Criacao'])
        self.tabela_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.txt_titulo)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.tabela_notas.cellDoubleClicked.connect(self.carrega_dados)
        self.popula_tabela_notas()
        self.atualiza_nota()

    def salvar_nota(self):
        db = Database()

        nota = Nota(
            id=self.lbl_id.text(),
            titulo=self.txt_titulo.text(),
            nota=self.txt_nota.toPlainText(),
            data_criacao=str(datetime.today().strftime('%d-%m-%Y'))
        )

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.registrar_nota(nota)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota efetuada')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao salvar nota')
                msg.setText(f'Erro ao salvar nota, tente novamente!')
                msg.exec()
        if self.btn_salvar.text() == 'Atualizar':
            retorno = db.atualizar_nota(nota)
            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota Atualizada com sucesso.')
                msg.setText(f'Atualizada com sucesso!')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText(f'erro ao atualizar nota, tente novamente')
                msg.exec()

        self.popula_tabela_notas()

    def remover_nota(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover nota')
        msg.setText('Esta nota será removida.')
        msg.setInformativeText(f'Você deseja remover esta nota?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = Database()

            if db.deletar_nota(self.lbl_id.text()) == 'OK':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Nota')
                nv_msg.setText('Nota removida com sucesso')
                nv_msg.exec()
                self.limpar_campos()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('Erro ao remover nota')
                nv_msg.exec()
        self.popula_tabela_notas()
        self.limpar_campos()

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget,QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        self.btn_remover.setVisible(False)
        self.btn_salvar.setText('Salvar')

    def popula_tabela_notas(self):
        self.tabela_notas.setRowCount(0)
        db = Database()
        lista_notas = db.consultar_todas_notas()
        self.tabela_notas.setRowCount(len(lista_notas))

        for linha, cliente in enumerate(lista_notas):
            for coluna, valor in enumerate(cliente):
                self.tabela_notas.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carrega_dados(self, row, column):
        self.lbl_id.setText(self.tabela_notas.item(row, 0).text())
        self.txt_titulo.setText(self.tabela_notas.item(row, 1).text())
        self.txt_nota.setText(self.tabela_notas.item(row, 2).text())

        self.btn_salvar.setText('Atualizar')
        self.btn_limpar.setVisible(False)
        self.btn_remover.setVisible(True)

    def atualiza_nota(self):
        db = Database()
        lista_notas = db.consultar_todas_notas()

        if len(lista_notas) != 0:
            self.lbl_id.setText(f'Bloco de notas {lista_notas}')
        else:
            self.lbl_id.setText(f'Bloco de notas')
            self.popula_tabela_notas()
            self.limpar_campos()

