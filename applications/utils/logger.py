# coding=utf-8

import logging
import logging.config
import applications.config

"""
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s用户输出的消息
"""

formatter_dict = {
    1: logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
    2: logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"),
    3: logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s - %(message)s"),
    4: logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(filename)s - Module:%(module)s - Func:%(funcName)s - %(message)s"),
    5: logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(filename)s - Module:%(module)s - Func:%(funcName)s - %(process)d - %(threadName)s - %(message)s")
}

loglevel_dict = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0
}


class Logger(object):
    def __init__(self, formatlevel, callfile):
        """
            指定日志文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        # Write log to file.

        self.logger = logging.getLogger(callfile)
        self.logger.setLevel(loglevel_dict[applications.config.LOG_DEFAULT_LEVEL])
        fh = logging.FileHandler(applications.config.LOG_FILE)
        fh.setFormatter(formatter_dict[int(formatlevel)])
        self.logger.addHandler(fh)

        # Print log to Console.

        #ch = logging.StreamHandler()
        #ch.setLevel(logging.ERROR)
        #ch.setFormatter(formatter_dict[int(loglevel)])
        #self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger(formatlevel=5, callfile=__file__).get_logger()
    logger.debug('test level5')
    logger1 = Logger(formatlevel=4, callfile=__file__).get_logger()
    logger1.info('test level4')
