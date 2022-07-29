# -*- coding: utf-8 -*-

import os
import sys
import errno
import platform
import logging
import logging.handlers

class STDLogger(object):
    """Simple Logging class
    Allow to log to standard syslog process or specific file if set 
    """
    def __init__(
        self,
        filename,
        level,
        name,
        cli,
        backup,
        when,
        pattern
    ):
        """Setup the logging handler instance used for log write.

        Args:
            filename (str|Path): Path to the log output file.
            level (int): Logging level
            name (str): Handler name
            cli (bool): Define if output is also sent to console
            backup (int): Number of backup file to keep
            when (str): Moment in day to rotate log file
            pattern (str): Logging pattern for event log

        """

        if name is None:
            name = __name__
        
        try:
            # Always set uppercase strings if needed
            self.level = self._get_level(level.upper()) if self._is_string(level) else int(level)
        except ValueError:
            # Set default value
            self.level = logging.WARNING

        self.logger = logging.getLogger(name)

        try:
            self.logger.setLevel(self.level)
        except ValueError:
            self.logger.setLevel(logging.WARNING)

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
                dirname = os.path.dirname(filename)
                if dirname and not os.path.isdir(dirname):
                    os.makedirs(dirname)
                # Create file if needed
                if not os.path.isfile(filename):
                    with open(filename, 'wt') as tmp:
                        pass
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

        self.cli = cli

    def _is_string(
        self,
        string
    ) -> bool:
        """Private method used to check if var is string, compliant with python2 & python3

        Args:
            string (str): the variable to check

        Returns:
            bool

        """
        try:
            basestring
        except NameError:
            basestring = str

        return isinstance(string, basestring)
        
    def _get_level(
        self,
        level
    ) -> int:
        """Private method to convert level string to logging int value

        Args:
            level (str): the string level to convert

        Returns:
            int

        """
        # Always set uppercase strings
        if not self._is_string(level):
            raise ValueError('Invalid level')
        
        level = level.upper()

        # Convert string level to logging int
        if level == "DEBUG":
            return logging.DEBUG
        elif level in ["INFO", "INFOS"]:
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        elif level == "CRITICAL":
            return logging.CRITICAL
        
        return self.level

    def _write_cli(
        self,
        prefix,
        message,
        color,
        light
    ) -> None:
        """Private method used to output a specific message to CLI using color

        Args:
            prefix (str|char): string set between brackets at the beginning of output message
            message (str): the message to output
            color (str): the color used to output message
            light (bool): flag used to trigger light mode on cli output

        Returns:
            None
        """
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
        
        sys.stdout.write("{color}[{p}] {msg}\033[0m\n".format(color=c, p=prefix, msg=message))

    