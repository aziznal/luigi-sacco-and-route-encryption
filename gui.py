from typing import Dict, List, Callable
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import *

import utils


class Gui(QMainWindow):

    def __init__(self, widget_type_id_dict: Dict[str, List[str]], gui_file_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.gui_file_path: str = utils.get_path_in_bundle_dir(gui_file_path)
        self.widget_type_id_dict: dict = utils.load_json(widget_type_id_dict)

        uic.loadUi(self.gui_file_path, self)

        # Stores all loaded widgets for easy access
        self._widget_objects = self._load_widget_objects()

        self.show()

    def _load_widget_objects(self) -> Dict[str, QWidget]:
        """
        Returns a dictionary of QWidgets mapped by their ids
        """
        widget_objects: Dict[str, QWidget] = {}

        for object_type, id_list in self.widget_type_id_dict.items():
            for object_id in id_list:

                # I use 'exec' here to avoid having to specify object type and
                # instead only define it in ids.json
                exec("widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")

        return widget_objects

    def get_widget(self, widget_id) -> QWidget:
        """
        Returns a QWidget that matches the given id
        """
        try:
            return self._widget_objects[widget_id]

        except Exception as e:
            traceback.print_exc()

    def add_event_listener(self, widget_id: str, on_event: Callable) -> None:
        
        self._widget_objects[widget_id].clicked.connect(on_event)
