# для переноса в нормальный формат сдачи

class History:

    def __init__(self):
        self._list_for_history = list()
        self._list_hotels = list()
        self._command = None
        self._time = None
        self._hotels = None

    def getter_history(self):
        return self._list_for_history

    def setter_for_not_hotels(self, msg, time):
        self._list_for_history.append([msg, time])

    def setter_for_hotels(self):
        self._list_for_history.append([self._command, self._time, self._hotels])
        self._command = None
        self._time = None
        self._hotels = None

    def else_setter_for_hotels(self):
        self._list_for_history.append([self._command, self._time])
        self._command = None
        self._time = None

    def setter_command_and_time(self, command, time):
        self._command = command
        self._time = time

    def setter_hotels(self, list_hotels):
        self._hotels = list_hotels


class_history = History()
