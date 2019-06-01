import logging
import logging.handlers


def splitStrIdToInteger(str_id_list):
    str_list = str_id_list.split(',')
    int_list = []
    for id in str_list:
        int_list.append(int(id))

    return int_list


def splitStr(str_list):
    return str_list.split(',')


#def getLogger(module):
#    LOG_FILENAME = Config.LOG_FILE
#    logger = logging.getLogger(module)
#    logger.setLevel(Config.LOG_DEFAULT_LEVEL)
#    formater = logging.Formatter("[%(levelname)s] - %(name)s - %(asctime)s: %(message)s")
#
#    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=102400, backupCount=5, encoding='utf8')
#    handler.setFormatter(formater)
#    logger.addHandler(handler)
#
#    return logger



