from typing import Callable

from PySide6.QtCore import QThread, Signal


class _StatusHistory(QThread):
    def __init__(self):
        super().__init__()
        self.progress_signal = Signal(str)

        self.history = []
        self.all_history_funcs = []
        self.newly_added_funcs = []

    def add_on_update_handler_full_history(self, func: Callable[[str], None]):
        self.all_history_funcs.append(func)

    def add_on_update_handler_newly_added(self, func: Callable[[str], None]):
        self.newly_added_funcs.append(func)

    def on_update(self):
        for func in self.newly_added_funcs:
            func(self.history[-1])
        for func in self.all_history_funcs:
            func('\n'.join(self.history))

    def add_record(self, record: str):
        self.history.append(record)
        self.on_update()


StatusHistory = _StatusHistory()
