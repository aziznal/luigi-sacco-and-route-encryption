from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

from gui import Gui

import utils


def create_main_window():
    
    widget_ids = "data/main-ids.json"
    gui_file_path = "data/main-menu.ui"
    kto_image_path = utils.get_path_in_bundle_dir("data/kto_logo.png")

    gui = Gui(widget_ids, gui_file_path)

    kto_image = QPixmap(kto_image_path)
    gui.get_widget("mainLabel").setPixmap(kto_image)

    gui.add_event_listener("exitButton", lambda: app.quit())
    
    return gui


def create_first_method_window():
    pass


def create_second_method_window():
    pass


if __name__ == '__main__':

    app = QApplication([])

    main_window = create_main_window()

    first_method_window = create_first_method_window()
    second_method_window = create_second_method_window()

    main_window.add_event_listener("firstMethodButton", lambda: print("Luigi Socco"))
    main_window.add_event_listener("secondMethodButton", lambda: print("Route Encryption"))

    app.exec_()
