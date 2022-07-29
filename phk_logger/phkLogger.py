# -*- coding: utf-8 -*-

import logging

from .stdLogger import STDLogger

class PHKLogger(STDLogger):
    """ProHacktive Logging class
    Set user-friendly methods to log event with specific log level
    """
    def __init__(
        self,
        filename=None,
        level=logging.WARNING,
        name=None,
        cli=False,
        backup=3,
        when="midnight",
        pattern=None
    ):
        """Setup the logging handler instance used for log write.

        Args:
            filename (str|Path): Path to the log output file (default: None).
            level (int): Logging level (default: WARNING).
            name (str): Handler name (default: None).
            cli (bool): Define if output is also sent to console (default: False).
            backup (int): Number of backup file to keep (default: 3).
            when (str): Moment in day to rotate log file (default: midnight).
            pattern (str): Logging pattern for event log (default: None).

        """

        super(PHKLogger, self).__init__(
            filename,
            level,
            name,
            cli,
            backup,
            when,
            pattern
            )
        
    def debug(
        self,
        msg,
        color=None,
        light=None
    ) -> None:
        """Shortcut to write debug event

        Args:
            msg (str): the message to write
            color (str): the color used for output to cli if set
            light (boolean): flag used to trigger light mode on cli output
        
        Returns:
            None
        """
        self.write(msg, level=logging.DEBUG, color=color, light=light)

    def info(
        self,
        msg,
        color=None,
        light=None
    ) -> None:
        """Shortcut to write info event

        Args:
            msg (str): the message to write
            color (str): the color used for output to cli if set
            light (boolean): flag used to trigger light mode on cli output
        
        Returns:
            None
        """
        self.write(msg, level=logging.INFO, color=color, light=light)

    def warning(
        self,
        msg,
        color=None,
        light=None
    ) -> None:
        """Shortcut to write warning event

        Args:
            msg (str): the message to write
            color (str): the color used for output to cli if set
            light (boolean): flag used to trigger light mode on cli output
        
        Returns:
            None
        """
        self.write(msg, level=logging.WARNING, color=color, light=light)

    def error(
        self,
        msg,
        color=None,
        light=None
    ) -> None:
        """Shortcut to write error event

        Args:
            msg (str): the message to write
            color (str): the color used for output to cli if set
            light (boolean): flag used to trigger light mode on cli output
        
        Returns:
            None
        """
        self.write(msg, level=logging.ERROR, color=color, light=light)

    def critical(
        self,
        msg,
        color=None,
        light=None
    ) -> None:
        """Shortcut to write critical event

        Args:
            msg (str): the message to write
            color (str): the color used for output to cli if set
            light (boolean): flag used to trigger light mode on cli output
        
        Returns:
            None
        """
        self.write(msg, level=logging.CRITICAL, color=color, light=light)

    def write(
        self,
        message,
        level=None,
        color=None,
        light=None
    ) -> None:
        """Write log message with specific level, allow override of color and light

        Args:
            message (str): The message to output
            level (int|str): the level of the event
            color (str): the color to use if cli flag is set
            light (bool): set the light version of cli color

        Returns:
            None
        """

        # Clean message
        message = str(message).rstrip()

        # Only log if there is a message (not just a new line)
        if message == "":
            return None

        # Autoset level if necessary
        if level is None:
            level = self.level

        # Convert string level to logging int
        if self._is_string(level):
            level = self._get_level(level)

        if level < self.level:
            return None

        # Output to with correct level
        if level == logging.DEBUG:
            def_color = "BLUE"
            def_light = True
            prefix = '*'
            self.logger.debug(message)
        elif level == logging.INFO:
            def_color = "GREEN"
            def_light = False
            prefix = '+'
            self.logger.info(message)
        elif level == logging.WARNING:
            def_color = "YELLOW"
            def_light = False
            prefix = '-'
            self.logger.warning(message)
        elif level == logging.ERROR:
            def_color = "RED"
            def_light = False
            prefix = '!'
            self.logger.error(message)
        elif level == logging.CRITICAL:
            def_color = "RED"
            def_light = True
            prefix = '!'
            self.logger.critical(message)
        else:
            raise Exception('Invalid log level')

        if color is None:
            color = def_color
        if light is None:
            light = def_light

        # Output to CLI if cli flag is set
        if self.cli:
            self._write_cli(prefix, message, color, light)