import logging
import logging.handlers

def create_logger():
    ''' Логирование успешных сообщений от клиентов в syslog.'''
    logger = logging.getLogger('chat_app')
    logger.setLevel('DEBUG')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

    sys_handler = logging.handlers.SysLogHandler(address='/dev/log')
    sys_handler.setLevel('DEBUG')
    sys_handler.setFormatter(formatter)

    logger.addHandler(sys_handler)

    return logger

