from sortinghat.command import Command


class ApiCommand(Command):
    """
    Abstract class to run commands from sortinghat.
    sortinghat uses a class hierarchy for commands like:

        object
            -> Command(object)
                -> Add(Command)

    In "Command" there are some methods with side effects like
        * display
        * error
        * warning

    All those methods write text to stdout or stderr.
    To avoid these side effects in our REST API context we create
    a new class ApiCommand(Command) to store the strings and provide
    new methods to get those strings afterwards.

    The new hierarchy for commands look like:

        object
            -> Command(object)
                -> ApiCommand(Command)
                    -> Add(ApiCommand)
    """

    def display(self, template, **kwargs):
        """
        display is available in the original base class (Command).
        This display method was overwritten to avoid the side effect
        of a stdout output.

        Original method can be found in the source code of sortinghat:
        https://github.com/MetricsGrimoire/sortinghat/blob/master/sortinghat/command.py#L51
        """
        self._display_vars = kwargs

    def error(self, msg):
        """
        error is available in the original base class (Command).
        This error method was overwritten to avoid the side effect
        of a stderr output.

        Original method can be found in the source code of sortinghat:
        https://github.com/MetricsGrimoire/sortinghat/blob/master/sortinghat/command.py#L62
        """
        self._error_vars = msg

    def warning(self, msg):
        """
        warning is available in the original base class (Command).
        This warning method was overwritten to avoid the side effect
        of a stderr output.

        Original method can be found in the source code of sortinghat:
        https://github.com/MetricsGrimoire/sortinghat/blob/master/sortinghat/command.py#L66
        """
        self._warning_vars = msg

    def get_display_vars(self):
        """
        Getter methods for data original passed to display()
        """
        return self._display_vars

    def get_error_vars(self):
        """
        Getter methods for data original passed to error()
        """
        return self._error_vars

    def get_warning_vars(self):
        """
        Getter methods for data original passed to warning()
        """
        return self._warning_vars