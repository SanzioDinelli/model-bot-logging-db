import logging
from functools import wraps
import logging.handlers
from time import time
from colorama import Fore, Back, Style
import os
from dotenv import load_dotenv; load_dotenv(os.path.join(os.getcwd(),".env"))

class Logger():
    def __init__(self, file_level, stream_level):
        SLACK_ON = False ### HABILITE CASO QUEIRA SER INFORMADO VIA SLACK
        #################################################################################### REMOVER OS LOGGERS DO FRAMEWORKS
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)
            logger.propagate = False

        #################################################################################### DEFINIR O PRÓPRIO LOGGER
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

        mail_handler  = logging.handlers.SMTPHandler(
            mailhost = ("smtp.gmail.com", 587),
            fromaddr = "sanzio.magalhae@gmail.com",
            toaddrs = ["sanzio.magalhae@gmail.com", "sanzio.magalhaes@hotmail.com"],
            subject = "Erro na aplicação!",
            credentials = ("sanzio.magalhae@gmail.com", os.environ.get("APP_PASSWORD")),
            secure = ()  # isso ativa o STARTTLS
        )
        mail_handler.setLevel(logging.CRITICAL)  # Envia e-mails apenas para logs de erro ou acima
        mail_formatter = logging.Formatter('[%(asctime)s] %(levelname)s em %(module)s: %(message)s')
        mail_handler.setFormatter(mail_formatter)

        slack_handler = SlackLogHandler(api_key=os.environ.get("API_SLACK_TOKEN"), channel=os.environ.get("SLACK_CHANNEL"))
        slack_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        slack_handler.setFormatter(formatter)
        

        class ColorFilter(logging.Filter):
            def filter(self, record):
                if record.levelno == logging.DEBUG:
                    record.levelname = f"{Fore.YELLOW}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
                elif record.levelno == logging.INFO:
                    record.levelname = f"{Fore.GREEN}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
                elif record.levelno == logging.WARNING:
                    record.levelname = f"{Fore.LIGHTRED_EX}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.LIGHTRED_EX}{record.msg}{Style.RESET_ALL}"
                elif record.levelno == logging.ERROR:
                    record.levelname = f"{Fore.RED}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
                elif record.levelno == logging.CRITICAL:
                    record.levelname = f"{Back.RED}{record.levelname}{Style.RESET_ALL}"
                    record.msg = f"{Back.RED}{record.msg}{Style.RESET_ALL}"
                return True

        
        logger.addHandler(mail_handler)
        logger.addHandler(file_handler)
        stream_handler.addFilter(ColorFilter())
        logger.addHandler(stream_handler)
        if SLACK_ON:
            logger.addHandler(slack_handler) 
        
        self.logger = logger

    def call_log(self, func):
        @wraps(func) # Preserva os metadados da função original
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(f"executando - {func.__qualname__}")
                inicio = time()
                response = func(*args, **kwargs) ### MÉTODO AQUI
                fim = time()
                self.logger.debug(f"encerrando método: duração - {float(fim - inicio):.2f} segundos\n")
                return response
            except Exception as error:
                fim = time()
                self.logger.error(f"Erro na função '{func.__name__}': {error}")
                self.logger.debug(f"encerrando método: duração - {float(fim - inicio):.2f} segundos\n")
        return wrapper

import slack
class SlackLogHandler(logging.Handler):
    def __init__(self, api_key, channel):
        super().__init__()
        self.channel = channel
        self.client = slack.WebClient(token=api_key)
    
    def emit(self, record):
        message = self.format(record)
        self.client.chat_postMessage(channel=self.channel,text=message)


