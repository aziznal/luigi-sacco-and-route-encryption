from gui import Gui

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap



if __name__ == '__main__':

    app = QApplication([])

    widget_ids = "data/main-ids.json"
    gui_file_path = "data/main-menu.ui"

    gui = Gui(widget_ids, gui_file_path)

    kto_image = QPixmap("data/kto_logo.png")
    gui.get_widget("mainLabel").setPixmap(kto_image)

    gui.add_event_listener("exitButton", exit)

    app.exec_()
