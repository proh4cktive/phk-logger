# -*- coding: utf-8 -*-

import os
import sys
import errno
import platform
import logging
import logging.handlers


class PHKLogger(object):
    """Simple Logging class
    Allow to log to standard syslog process or specific file if set 
    """
    def __init__(self, filename=None, level=logging.WARNING, name=None, cli=False, backup=3, when="midnight", pattern=None):
        if name is None:
            name = __name__

        try:
            self.level = int(level)
        except ValueError:
            self.level = logging.INFO

        self.logger = logging.getLogger(name)

        # Default behavior
        if filename is None:
            # Set syslog handler
            current = platform.system()
            if current == 'Linux':
                target = '/dev/log'
            elif current == 'Darwin':
                target = '/var/run/syslog'
            else:
                raise NotImplementedError('Sorry unsupported plateform.')
            handler = logging.handlers.SysLogHandler(target)
        
        # If filename is set
        else:
            try:
                # Create directory if needed
                if not os.path.isdir(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
            except OSError as err:
                raise Exception(err)

            try:
                # Set a time rotating handler
                handler = logging.handlers.TimedRotatingFileHandler(filename, when=when, backupCount=backup)
            except IOError:
                raise Exception('Unable to set Time Rotating Log file: {f}'.format(f=filename))

        if pattern is None:
            pattern = '%(name)s %(asctime)s %(levelname)-8s %(message)s'

        formatter = logging.Formatter(pattern)
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
        self.logger.setLevel(self.level)

        self.cli = cli

    def __is_string(self, string):
        try:
            return isinstance(string, str)
        except NameError:
            return isinstance(string, basestring)

    def debug(self, msg, color=None, light=None):
        """Shortcut to debug message
        """
        self.write(msg, level=logging.DEBUG, color=color, light=light)

    def info(self, msg, color=None, light=None):
        """Shortcut to info message
        """
        self.write(msg, level=logging.INFO, color=color, light=light)

    def warning(self, msg, color=None, light=None):
        """Shortcut to warning message
        """
        self.write(msg, level=logging.WARNING, color=color, light=light)

    def error(self, msg, color=None, light=None):
        """Shortcut to error message
        """
        self.write(msg, level=logging.ERROR, color=color, light=light)

    def critical(self, msg, color=None, light=None):
        """Shortcut to critical message
        """
        self.write(msg, level=logging.CRITICAL, color=color, light=light)

    def write(self, message, level=None, color=None, light=None):
        """Accept log message with level set with string or logging int
        """

        # Clean message
        message = str(message).rstrip()

        # Only log if there is a message (not just a new line)
        if message == "":
            return True

        # Autoset level if necessary
        if level is None:
            level = self.level

        # Convert string level to logging int
        if self.__is_string(level):
            level = level.upper()
            if level == "DEBUG":
                level = logging.DEBUG
            elif level in ["INFO", "INFOS"]:
                level = logging.INFO
            elif level == "WARNING":
                level = logging.WARNING
            elif level == "ERROR":
                level = logging.ERROR
            elif level == "CRITICAL":
                level = logging.CRITICAL
            else:
                level = self.level

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
            color = color.upper()
            # Position color based on level if not forced
            c = '\033[1' if light else '\033[0'
            if color == 'BLACK':
                c += ';30m'
            elif color == 'BLUE':
                c += ';34m'
            elif color == 'GREEN':
                c += ';32m'
            elif color == 'CYAN':
                c += ';36m'
            elif color == 'RED':
                c += ';31m'
            elif color == 'PURPLE':
                c += ';35m'
            elif color == 'YELLOW':
                c += ';33m'
            elif color == 'WHITE':
                c += ';37m'
            else:
                # No Color
                c += 'm'
            
            if level >= self.level:
                sys.stdout.write("{color}[{p}] {msg}\033[0m\n".format(color=c, p=prefix, msg=message))
