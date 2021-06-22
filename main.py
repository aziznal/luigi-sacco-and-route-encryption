import PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

from gui import Gui

from logic.luigi_sacco import luigi_sacco_encrypt, luigi_sacco_decrypt
from logic.route_encryption import route_encrypt, route_decrypt, get_potential_table_sizes

import utils


def center_window(window: Gui) -> None:
    centered_x = screen_geometry.center().x() - window.width()//2
    centered_y = screen_geometry.center().y() - window.height()//2

    window.move(centered_x, centered_y)


def create_main_window():

    widget_ids = "assets/main-ids.json"
    gui_file_path = "assets/main-menu.ui"
    kto_image_path = utils.get_path_in_bundle_dir("assets/kto_logo.png")

    gui = Gui(widget_ids, gui_file_path)

    center_window(gui)

    kto_image = QPixmap(kto_image_path)
    gui.get_widget("mainLabel").setPixmap(kto_image)

    gui.add_event_listener("exitButton", lambda: app.quit())

    return gui


def create_first_method_window(main_window: Gui):
    widget_ids = "assets/first-method-ids.json"
    gui_file_path = "assets/first-method.ui"

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
    widget_ids = "assets/second-method-ids.json"
    gui_file_path = "assets/second-method.ui"

    gui = Gui(widget_ids, gui_file_path)

    gui.hide()

    def show_main_window():
        gui.hide()

        center_window(main_window)

        main_window.show()

        main_window.activateWindow()

    # Adding images for Route Visualization
    routes_image_path = utils.get_path_in_bundle_dir("assets/routes.png")
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



def get_chosen_table_size(input_text, window: Gui):
    
    if len(input_text) <= 0:
        return

    sizes, _ = get_potential_table_sizes(len(input_text))

    return sizes[ window.get_widget('arraySizeComboBox').currentIndex() ]


def run_route_encryption(window: Gui):

    get = lambda x: window.get_widget(x)

    # Input Text
    input_text = get('inputTextEdit').toPlainText()

    if len(input_text) <= 0:
        return

    # Table Size
    table_size = get_chosen_table_size(input_text, window)

    # Encrypt vs. Decrypt
    encrypt = get('encryptRadioButton').isChecked()
    decrypt = get('decryptRadioButton').isChecked()

    # Final output message which goes to output box
    output = ""

    if encrypt:
        output = route_encrypt(input_text, table_size)

    elif decrypt:
        output = route_decrypt(input_text, table_size)


    get('outputTextEdit').setPlainText(output)


def reset_route_encryption(window: Gui):

    get = lambda x: window.get_widget(x)

    get('inputTextEdit').clear()
    get('outputTextEdit').clear()
    get('arraySizeComboBox').clear()
    

def populate_combobox(combobox, message):

    combobox.clear()
    if len(message) <= 0:
        return

    # Populate combobox with list of sizes
    sizes, optimal_size = get_potential_table_sizes(len(message))
    
    for size in sizes:
        if size == optimal_size or size == optimal_size[::-1]:
            combobox.addItem(f"{size[0]} x {size[1]} (Recommended)")

        else:
            combobox.addItem(f"{size[0]} x {size[1]}")


def add_route_encryption_hooks(window: Gui):
    get = lambda x: window.get_widget(x)

    # Set Encrypt as default option
    get('encryptRadioButton').setChecked(True)

    # Set drop-select to have no elements at the start
    get('arraySizeComboBox').clear()


    # As text gets typed, the table size combo-box gets filled with new values
    get('inputTextEdit').textChanged.connect(
        lambda: populate_combobox(get('arraySizeComboBox'), get('inputTextEdit').toPlainText())
    )

    # Run and Reset Button Listeners
    window.add_event_listener("runButton", lambda: run_route_encryption(window))
    window.add_event_listener("resetButton", lambda: reset_route_encryption(window))



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

    
    # TODO
    #   If message length is prime, either inform user or automatically add
    #   extra letter to make its length non-prime


    # TODO: 
    #   Make sure to inform user to provide correct table size when
    #   decrypting a message

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


    add_luigi_sacco_hooks(first_method_window)

    add_route_encryption_hooks(second_method_window)

    app.exec_()
