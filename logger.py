import logging
from functools import wraps
from time import time
from colorama import Fore, Back, Style

class Logger():
    def __init__(self, file_level, stream_level):
        ### REMOVER O LOGGER DO WEBDRIVER 
        selenium_logger = logging.getLogger('selenium')
        selenium_logger.setLevel(level=logging.CRITICAL)
        selenium_logger.propagate = False

        selenium_webdriver_logger = logging.getLogger('selenium.webdriver')
        selenium_webdriver_logger.setLevel(level=logging.CRITICAL)
        selenium_webdriver_logger.propagate = False

        urllib_logger = logging.getLogger('urllib3.connectionpool')
        urllib_logger.setLevel(logging.CRITICAL)
        urllib_logger.propagate = False

        selenium_remote_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_remote_logger.setLevel(logging.CRITICAL)
        selenium_remote_logger.propagate = False

        ### DEFINIR O PRÓPRIO LOGGER
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)

        stream_handler = logging.StreamHandler( )
        stream_handler.setLevel(stream_level)
        stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(stream_formatter)

        logging.Handler

        class ColorFilter(logging.Filter):
            def filter(self, record):
                if record.levelno == logging.DEBUG:
                    record.levelname = f"{Fore.YELLOW}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
                if record.levelno == logging.INFO:
                    record.levelname = f"{Fore.GREEN}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
                if record.levelno == logging.WARNING:
                    record.levelname = f"{Fore.LIGHTRED_EX}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.LIGHTRED_EX}{record.msg}{Style.RESET_ALL}"
                if record.levelno == logging.ERROR:
                    record.levelname = f"{Fore.RED}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
                if record.levelno == logging.CRITICAL:
                    record.levelname = f"{Back.RED}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Back.RED}{record.msg}{Style.RESET_ALL}"
                return True

        stream_handler.addFilter(ColorFilter())
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        self.logger = logger

    def call_log(self, func):
        @wraps(func) # Preserva os metadados da função original
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(f"executando - {__file__.split("\\")[-1]}:{func.__name__}")
                inicio = time()
                response = func(*args, **kwargs) ### MÉTODO AQUI
                fim = time()
                self.logger.debug(f"encerrando método: duração - {float(fim - inicio):.2f} segundos\n")
                return response
            except Exception as error:
                fim = time()
                logging.error(f"Erro na função '{func.__name__}': {error}")
                self.logger.debug(f"encerrando método: duração - {float(fim - inicio):.2f} segundos\n")
        return wrapper