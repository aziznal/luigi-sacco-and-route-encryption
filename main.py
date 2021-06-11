from gui import Gui

from PyQt5.QtWidgets import QApplication



if __name__ == '__main__':

    app = QApplication([])


    widget_ids = "data/example-ids.json"
    gui_file_path = "data/example-gui.ui"

    gui = Gui(widget_ids, gui_file_path)

    gui.add_event_listener(
        widget_id="exitButton",
        on_event=lambda: exit()
    )


    def button_onclick():
        gui.get_widget("mainLabel").setText("Congratulations! You have clicked a button")

    gui.add_event_listener(
        widget_id="mainButton",
        on_event=lambda: button_onclick()
    )


    app.exec_()
