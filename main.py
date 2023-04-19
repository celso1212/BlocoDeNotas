import sys
from PySide6.QtWidgets import QApplication

from controller.nota_dao import Database
from view.tela_principal import MainWindow

db = Database()
db.connect()
db.create_table_nota()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()