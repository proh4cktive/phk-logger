# -*- coding: utf-8 -*-

import os
import pytest
import logging

from phk_logger import __version__
from phk_logger import PHKLogger as Logger

@pytest.fixture(scope='session')
def log_file(request):
    # Will be executed before the first test
    f = open(request.param, 'wt')
    f.close()

    f = open(request.param, 'rt')
    yield f
    # Will be executed after the last test
    f.close()
    # Remove file
    os.remove(request.param)

class TestIt:
    def test_version(self):
        assert __version__ == '0.1.4'

    def test_init(self, caplog):
        logger = Logger()
        assert True
        caplog.set_level(logging.WARNING)
        logger.debug('Check DEBUG')
        assert caplog.record_tuples == []
        logger.info('Check INFOS')
        assert caplog.record_tuples == []
        logger.warning('Check WARNING')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.WARNING, "Check WARNING")]
        caplog.clear()
        logger.error('Check ERROR')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.ERROR, "Check ERROR")]
        caplog.clear()
        logger.critical('Check CRITICAL')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.CRITICAL, "Check CRITICAL")]
        caplog.clear()
        
        logger.write('Check DEBUG', level='debug')
        assert caplog.record_tuples == []
        caplog.clear()
        logger.write('Check INFO', level='info')
        assert caplog.record_tuples == []
        caplog.clear()
        logger.write('Check INFOS', level='infos')
        assert caplog.record_tuples == []
        caplog.clear()
        logger.write('Check WARNING', level='warning')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.WARNING, "Check WARNING")]
        caplog.clear()
        logger.write('Check ERROR', level='error')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.ERROR, "Check ERROR")]
        caplog.clear()
        logger.write('Check CRITICAL', level='critical')
        assert caplog.record_tuples == [("phk_logger.phkLogger", logging.CRITICAL, "Check CRITICAL")]
        
        logger = None

    def test_named(self, caplog):
        logger = Logger(name='mytest')
        assert True
        caplog.set_level(logging.WARNING)
        logger.debug('Check DEBUG')
        assert caplog.record_tuples == []
        logger.info('Check INFOS')
        assert caplog.record_tuples == []
        logger.warning('Check WARNING')
        assert caplog.record_tuples == [("mytest", logging.WARNING, "Check WARNING")]

        logger = None

    @pytest.mark.parametrize('log_file', ['mytest.log','./.mytest.log','/tmp/mytest.log'], indirect=True)
    def test_filename(self, log_file):
        logger = Logger(filename=log_file.name)
        assert os.path.exists(log_file.name)

        logger.info('Check INFO')
        assert log_file.read() == ''
        logger.warning('Check WARNING')
        # Get last line in file
        for line in log_file:
            pass
        assert line.startswith("phk_logger.phkLogger ")
        assert line.endswith(" WARNING  Check WARNING\n")

        logger = None

    def test_cli(self, capsys):
        logger = Logger(cli=True)
        assert True

        logger.debug('Check DEBUG')
        captured = capsys.readouterr()
        assert captured.out == ''

        logger.info('Check INFO')
        captured = capsys.readouterr()
        assert captured.out == ''

        logger.warning('Check WARNING')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[0;33m[-] Check WARNING\x1b[0m\n"

        logger.error('Check ERROR')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[0;31m[!] Check ERROR\x1b[0m\n"

        logger.critical('Check CRITICAL')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[1;31m[!] Check CRITICAL\x1b[0m\n"

        logger = None

    def test_debug(self, capsys):
        logger = Logger(name='mytest', cli=True, level='debug')
        assert True
        
        # logger.debug('Check DEBUG')
        # captured = capsys.readouterr()
        # assert captured.out == "\x1b[1;34m[*] Check DEBUG\x1b[0m\n"

        logger.info('Check INFO')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[0;32m[+] Check INFO\x1b[0m\n"

        logger.warning('Check WARNING')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[0;33m[-] Check WARNING\x1b[0m\n"

        logger.error('Check ERROR')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[0;31m[!] Check ERROR\x1b[0m\n"

        logger.critical('Check CRITICAL')
        captured = capsys.readouterr()
        assert captured.out == "\x1b[1;31m[!] Check CRITICAL\x1b[0m\n"

        logger = None

    def test_pattern(self, capsys):
        logger = Logger(name='my_test', pattern='%(name)s %(message)s')
        assert True

        logger = None