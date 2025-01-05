from PyQt5.QtWidgets import QApplication
from app import HitsterApp
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HitsterApp()
    window.show()
    sys.exit(app.exec_())