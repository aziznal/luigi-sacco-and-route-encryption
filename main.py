from typing import Callable, Literal, Tuple

from PyQt5.QtWidgets import QApplication, QComboBox, QWidget
from PyQt5.QtGui import QPixmap


from gui import Gui

from logic.luigi_sacco import luigi_sacco_encrypt, luigi_sacco_decrypt, confirm_text_in_correct_lang, format_key_and_input_text
from logic.route_encryption import route_encrypt, route_decrypt, get_potential_table_sizes

import utils

ENCRYPT, DECRYPT = (True, False), (False, True)


def center_window(window: Gui) -> None:
    """
    Center the given window on the screen
    """
    centered_x = screen_geometry.center().x() - window.width()//2
    centered_y = screen_geometry.center().y() - window.height()//2

    window.move(centered_x, centered_y)



def create_main_window() -> Gui:
    """
    Creates app main window from which user can go to luigi sacco or route encryption windows
    """

    widget_ids = "assets/main-ids.json"
    gui_file_path = "assets/main-menu.ui"
    kto_image_path = utils.get_path_in_bundle_dir("assets/kto_logo.png")

    gui = Gui(widget_ids, gui_file_path)

    center_window(gui)

    kto_image = QPixmap(kto_image_path)
    gui.get_widget("mainLabel").setPixmap(kto_image)

    gui.add_event_listener("exitButton", lambda: app.quit())

    return gui



def create_error_message_window() -> Gui:
    """
    Creates a small error message whose contents can be tuned to inform the user
    of an error
    """

    widget_ids = "assets/error-message.json"
    gui_file_path = "assets/error-message.ui"

    gui = Gui(widget_ids, gui_file_path)

    # Hidden by default
    gui.hide()

    center_window(gui)

    # Set the okay button to hide the window when clicked
    gui.add_event_listener('okayButton', lambda: gui.hide())

    return gui



def display_error_message( error_message_window: Gui, title: str, content: str, solution: str) -> None:
    """
    Shows error dialog.
    """
    error_message_window.get_widget('errorNameLabel').setText(title)
    error_message_window.get_widget('errorMessageLabel').setText(content)
    error_message_window.get_widget('errorSolutionLabel').setText(solution)

    center_window(error_message_window)

    error_message_window.show()

    error_message_window.activateWindow()


def goto_window(source: Gui, destination: Gui) -> None:
    """
    Hides source gui and centers then shows the destination gui
    """
    source.hide()

    center_window(destination)

    destination.activateWindow()

    destination.show()



def create_luigi_sacco_window(main_window: Gui, show_error: Callable[[str, str, str], None]) -> Gui:
    """
    Creates a submenu where user can use luigi sacco encryption / decrypytion
    """
    widget_ids = "assets/first-method-ids.json"
    gui_file_path = "assets/first-method.ui"

    gui = Gui(widget_ids, gui_file_path, show_error)

    gui.hide()

    gui.add_event_listener("backButton", lambda: goto_window(gui, main_window))

    return gui


def create_route_encryption_window(main_window: Gui, show_error: Callable[[str, str, str], None]) -> Gui:
    """
    Creates window where user can use route encryption / decryption according to E4 & B3 Routes
    """
    widget_ids = "assets/second-method-ids.json"
    gui_file_path = "assets/second-method.ui"

    gui = Gui(widget_ids, gui_file_path, show_error)

    # Make this window hidden by default
    gui.hide()

    # Adding images for Route Visualization
    routes_image_path = utils.get_path_in_bundle_dir("assets/routes.png")
    routes_image = QPixmap(routes_image_path)

    gui.get_widget("routesLabel").setPixmap(routes_image)

    gui.add_event_listener("backButton", lambda: goto_window(gui, main_window))

    return gui



def get_luigi_sacco_language(get: Callable[[str], QWidget]) -> Literal["EN", "TR"]:
    """
    Extracts and returns chosen language from Luigi Sacco Gui
    """
    return "EN" if get('englishRadioButton').isChecked() else "TR"


def get_luigi_sacco_input(get: Callable[[str], QWidget]) -> Tuple[str, str]:
    """
    Extracts and returns key and text which user has given in Gui.

    Raises ValueError if either key or text are empty
    """

    key = get('keyTextEdit').toPlainText()
    
    plain_text = get('inputTextEdit').toPlainText()

    if key == "" or plain_text == "":
        raise ValueError("Key or Plain Text not given")
    
    return key, plain_text


def get_selected_action(get: Callable[[str], QWidget]) -> Tuple[bool, bool]:
    """
    Returns whether given gui is in encrypt or decrypt state.
    """
    encrypt = get('encryptRadioButton').isChecked()
    decrypt = get('decryptRadioButton').isChecked()

    return encrypt, decrypt


def run_luigi_sacco(window: Gui) -> None:
    """
    Function to run when Run Button is clicked in Luigi Sacco window.
    
    Runs luigi sacco encryption / decryption on the given key and
    input text and takes given language into account.

    Sets the output of the algorithm as the content of the output box
    """

    # Shortcut for ops in this function
    get = lambda x: window.get_widget(x)

    language = get_luigi_sacco_language(get)

    try:
        key, plain_text = get_luigi_sacco_input(get)

    except ValueError:
        window.show_error(
            title="Empty Key or Input Text",
            content="Cannot run program without both Key and Input Text present.",
            solution="Please fill in both of these fields and try again"
        )

        return

    action = get_selected_action(get)

    output = ""


    formatted_key, formatted_plain_text = format_key_and_input_text(key, plain_text)
    
    # Confirm Language has been correctly chosen
    try:
        confirm_text_in_correct_lang(formatted_key, language)
    except ValueError:
        window.show_error(
            title="Key has invalid characters",
            content="Your key includes characters that do not belong in your chosen language",
            solution="Remove any characters than don't belong to your chosen language and try again"
        )

        return

    try:
        confirm_text_in_correct_lang(formatted_plain_text, language)
    except ValueError:
        window.show_error(
            title="Plain Text has invalid characters",
            content="Your Plain Text includes characters that do not belong in your chosen language",
            solution="Remove any characters than don't belong to your chosen language and try again"
        )

        return

    if action == ENCRYPT:
        output = luigi_sacco_encrypt(key, plain_text, language)

    elif action == DECRYPT:
        output = luigi_sacco_decrypt(key, plain_text, language)

    get('outputTextEdit').setPlainText(output)


def reset_luigi_sacco(window: Gui) -> None:
    """
    Resets gui in luigi sacco to blank state
    """
    window.get_widget('keyTextEdit').clear()
    window.get_widget('inputTextEdit').clear()
    window.get_widget('outputTextEdit').clear()



def get_chosen_table_size(input_text: str, get: Callable[[str], QWidget]) -> Tuple[int, int]:
    """
    Returns chosen table size from gui according to given input text
    """

    if len(input_text) <= 0:
        return (0, 0)

    sizes, _ = get_potential_table_sizes(len(input_text))

    return sizes[get('arraySizeComboBox').currentIndex()]


def get_route_encryption_input(get: Callable[[str], QWidget]) -> Tuple[str, Tuple[int, int]]:
    """
    Extracts and returns input text and table size from Route Encryption Gui
    """
    input_text = get('inputTextEdit').toPlainText()

    table_size = get_chosen_table_size(input_text, get)

    return input_text, table_size


def run_route_encryption(window: Gui) -> None:
    """
    Function to run when Run Button is clicked in Route Encryption window.
    
    Runs route encryption / decryption on the given key and
    input text and takes given language into account.

    Sets the output of the algorithm as the content of the output box
    """

    # Shortcut for ops in this function
    def get(x): return window.get_widget(x)

    input_text, table_size = get_route_encryption_input(get)

    if len(input_text) == 0:
        window.show_error(
            title="Cannot Encrypt / Decrypt Empty Message",
            content="You attempted to start the program with no input text",
            solution="Enter at least one character in input field and try again"
        )
        return

    elif len(input_text) > 50:
        window.show_error(
            title="Your input is too long",
            content="Maximum allowed is 50 characters",
            solution=f"You have entered {len(input_text)} characters. Please make sure your input is less than 50 characters."
        )

        return

    if utils.is_prime(len(input_text)):
        window.show_error(
            title="Warning! Text Length is Prime",
            content=f"Your input text has a prime length of {len(input_text)} characters",
            solution="To get better performance using this encryption method, add another letter to your message."
        )


    # Encrypt vs. Decrypt
    action = get_selected_action(get)

    # Final output message which goes to output box
    output = ""

    if action == ENCRYPT:
        output = route_encrypt(input_text, table_size)

    elif action == DECRYPT:
        output = route_decrypt(input_text, table_size)

    get('outputTextEdit').setPlainText(output)


def reset_route_encryption(window: Gui) -> None:
    """
    Resets route encryption gui to blank state
    """

    def get(x): return window.get_widget(x)

    get('inputTextEdit').clear()
    get('outputTextEdit').clear()
    get('arraySizeComboBox').clear()


def populate_combobox(combobox: QComboBox, get_message: Callable[[], str]) -> None:
    """
    Populates given combobox with potential tables sizes for the given message.
    """

    combobox.clear()

    message = get_message()

    if len(message) <= 0:
        return

    # Populate combobox with list of sizes
    sizes, optimal_size = get_potential_table_sizes(len(message))

    for size in sizes:
        if size == optimal_size or size == optimal_size[::-1]:
            combobox.addItem(f"{size[0]} x {size[1]} (Recommended)")

        else:
            combobox.addItem(f"{size[0]} x {size[1]}")



def add_route_encryption_hooks(window: Gui) -> None:
    """
    Hooks Route Encryption Gui with its Logic
    """
    def get(x): return window.get_widget(x)

    # Set Encrypt as default option
    get('encryptRadioButton').setChecked(True)

    # Set drop-select to have no elements at the start
    get('arraySizeComboBox').clear()

    input_text = get('inputTextEdit').toPlainText()
    combobox = get('arraySizeComboBox')

    # As text gets typed, the table size combo-box gets filled with new values
    get('inputTextEdit').textChanged.connect(
        lambda: populate_combobox(combobox, lambda: get('inputTextEdit').toPlainText())
    )

    # Run and Reset Button Listeners
    window.add_event_listener(
        "runButton",
        lambda: run_route_encryption(window)
    )

    window.add_event_listener(
        "resetButton",
        lambda: reset_route_encryption(window)
    )


def add_luigi_sacco_hooks(window: Gui) -> None:
    """
    Hooks Luigi Sacco Gui with its Logic
    """

    # Shortcuts for ops in this function
    get = lambda x: window.get_widget(x)

    # Check English by default
    get('englishRadioButton').setChecked(True)

    # Check Encrypt by default
    get('encryptRadioButton').setChecked(True)

    # Set listeners for RUN and RESET buttons
    window.add_event_listener('runButton', lambda: run_luigi_sacco(window))
    window.add_event_listener('resetButton', lambda: reset_luigi_sacco(window))

    # TODO: add information section about luigi sacco and hook it up here


if __name__ == '__main__':

    # TODO:
    #   Add section where message is displayed in E4 Matrix form

    app = QApplication([])

    screen_geometry = QApplication.desktop().screenGeometry()
    SCREEN_WIDTH = screen_geometry.width()
    SCREEN_HEIGHT = screen_geometry.height()

    main_window = create_main_window()
    error_dialog = create_error_message_window()

    show_error = lambda title, content, solution: display_error_message(error_dialog, title, content, solution)

    luigi_sacco_window = create_luigi_sacco_window(main_window, show_error)
    route_encryption_window = create_route_encryption_window(main_window, show_error)

    main_window.add_event_listener(
        "firstMethodButton",
        lambda: goto_window(main_window, luigi_sacco_window)
    )

    main_window.add_event_listener(
        "secondMethodButton",
        lambda: goto_window(main_window, route_encryption_window)
    )

    add_luigi_sacco_hooks(luigi_sacco_window)

    add_route_encryption_hooks(route_encryption_window)

    app.exec_()
