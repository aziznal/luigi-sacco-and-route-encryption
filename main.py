from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

from gui import Gui

from playground.main import luigi_sacco_encrypt, luigi_sacco_decrypt

import utils


def center_window(window: Gui) -> None:
    centered_x = screen_geometry.center().x() - window.width()//2
    centered_y = screen_geometry.center().y() - window.height()//2

    window.move(centered_x, centered_y)


def create_main_window():

    widget_ids = "data/main-ids.json"
    gui_file_path = "data/main-menu.ui"
    kto_image_path = utils.get_path_in_bundle_dir("data/kto_logo.png")

    gui = Gui(widget_ids, gui_file_path)

    center_window(gui)

    kto_image = QPixmap(kto_image_path)
    gui.get_widget("mainLabel").setPixmap(kto_image)

    gui.add_event_listener("exitButton", lambda: app.quit())

    return gui


def create_first_method_window(main_window: Gui):
    widget_ids = "data/first-method-ids.json"
    gui_file_path = "data/first-method.ui"

    gui = Gui(widget_ids, gui_file_path)

    gui.hide()

    def show_main_window():
        gui.hide()

        center_window(main_window)

        main_window.show()

        main_window.activateWindow()

    gui.add_event_listener("backButton", show_main_window)

    return gui


def create_second_method_window(main_window):
    widget_ids = "data/second-method-ids.json"
    gui_file_path = "data/second-method.ui"

    gui = Gui(widget_ids, gui_file_path)

    gui.hide()

    def show_main_window():
        gui.hide()

        center_window(main_window)

        main_window.show()

        main_window.activateWindow()

    # Adding images for Route Visualization
    routes_image_path = utils.get_path_in_bundle_dir("data/routes.png")
    routes_image = QPixmap(routes_image_path)

    gui.get_widget("routesLabel").setPixmap(routes_image)

    gui.add_event_listener("backButton", show_main_window)

    return gui



def run_luigi_sacco(window: Gui):

    get = lambda x: window.get_widget(x)

    language = "EN" if get('englishRadioButton').isChecked() else "TR"
    key = get('keyTextEdit').toPlainText()
    plain_text = get('inputTextEdit').toPlainText()

    if key == "" or plain_text == "":
        return

    encrypt = get('encryptRadioButton')
    decrypt = get('decryptRadioButton')

    output = ""

    if encrypt.isChecked():
        output = luigi_sacco_encrypt(key, plain_text, language)

    elif decrypt.isChecked():
        output = luigi_sacco_decrypt(key, plain_text, language)


    get('outputTextEdit').setPlainText(output)


def reset_luigi_sacco(window: Gui):
    window.get_widget('keyTextEdit').clear()
    window.get_widget('inputTextEdit').clear()
    window.get_widget('outputTextEdit').clear()



def add_luigi_sacco_hooks(window: Gui):

    # Check English and Encrypt by default
    window.get_widget('encryptRadioButton').setChecked(True)
    window.get_widget('englishRadioButton').setChecked(True)

    # Set listeners for RUN and RESET buttons
    window.add_event_listener('runButton', lambda: run_luigi_sacco(window))
    window.add_event_listener('resetButton', lambda: reset_luigi_sacco(window))

    # TODO: add information section about luigi sacco and hook it up here


if __name__ == '__main__':

    # TODO
    #   add error window that can be called on user error and display a
    #   certain message

    app = QApplication([])

    screen_geometry = QApplication.desktop().screenGeometry()
    SCREEN_WIDTH = screen_geometry.width()
    SCREEN_HEIGHT = screen_geometry.height()

    main_window = create_main_window()
    first_method_window = create_first_method_window(main_window)
    second_method_window = create_second_method_window(main_window)

    def show_method_window(method_window):
        main_window.hide()

        center_window(method_window)

        method_window.show()
        method_window.activateWindow()

    main_window.add_event_listener(
        "firstMethodButton", lambda: show_method_window(first_method_window))

    main_window.add_event_listener(
        "secondMethodButton", lambda: show_method_window(second_method_window))


    # Add hooks to luigi sacco
    add_luigi_sacco_hooks(first_method_window)

    app.exec_()
