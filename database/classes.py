class History:
    """
    Базовый класс для вывода истории пользователя
    """

    def __init__(self):
        self._list_for_history = list()
        self._list_hotels = list()
        self._command = None
        self._time = None
        self._hotels = None

    def getter_history(self) -> list:
        """
        Геттер для получения информации истории (команда, время, выводимые отели.)
        :return: _list_for_history
        :rtype: list
        """
        return self._list_for_history

    def setter_for_not_hotels(self, msg: str, time: str) -> None:
        """
        Сеттер для добавления в историю информацию о команде, не
        требующую вывод отелей
        """
        self._list_for_history.append([msg, time])

    def setter_for_hotels(self) -> None:
        """
        Сеттер для добавления в историю информацию о команде,
        требующую вывод отелей
        """
        self._list_for_history.append([self._command, self._time, self._hotels])
        self._command = None
        self._time = None
        self._hotels = None

    def else_setter_for_hotels(self) -> None:
        """
        Сеттер для добавления в историю информацию о команде,
        требующую вывод отелей, но результат отелей - 0
        """
        self._list_for_history.append([self._command, self._time])
        self._command = None
        self._time = None

    def setter_command_and_time(self, command: str, time: str) -> None:
        """
        Сеттер для добавления информации о времени и команде,
        где требуется вывод отелей
        """
        self._command = command
        self._time = time

    def setter_hotels(self, list_hotels: list) -> None:
        """
        Сеттер для добавления информации о выводимых отелей
        """
        self._hotels = list_hotels


class_history = History()
