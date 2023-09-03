import sys
from PyQt5.QtWidgets import QApplication
from app import ReproductorDeMusica

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ReproductorDeMusica()
    ventana.show()
    sys.exit(app.exec_())
