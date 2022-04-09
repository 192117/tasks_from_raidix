import logging
import logging.handlers
from logging.handlers import SysLogHandler
from logging import Formatter

def create_logger():
    ''' Логирование успешных сообщений от клиентов в syslog.'''
    logger = logging.getLogger('chat_app')
    logger.setLevel(logging.INFO)

    format = '%(asctime)s - %(name)s - %(message)s'

    sys_handler = SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log') # Unix
    # sys_handler = logging.FileHandler('chat.log') # Windows
    sys_handler.setLevel('INFO')
    sys_handler.setFormatter(Formatter(fmt=format))

    logger.addHandler(sys_handler)

    return logger

