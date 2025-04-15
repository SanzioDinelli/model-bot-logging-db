from logger import Logger; from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from dao import Dao
from selenium import webdriver
import inspect

logger_agent = Logger(file_level=NOTSET, stream_level=DEBUG)
dao_agent = Dao()

CONDITION_1 = ""
CONDITION_2 = ""
CONDITION_3 = ""

class Bot():

    @logger_agent.call_log
    def __init__(self):
        print(f"Bot Instancializado, eis meus métodos:")
        methods_list = [method for method in Bot.__dict__.keys() if not method.startswith("__")]
        for key in methods_list:
                print("=>", key)

        condition_list = [CONDITION_1, CONDITION_2, CONDITION_3]

        dao_agent.create_custom_process_table(methods_list)
        dao_agent.create_custom_condition_table(condition_list)

    @logger_agent.call_log
    def instanciar_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        logger_agent.logger.info("Webdriver Instancializado")
        dao_agent.save_state(inspect.currentframe().f_code.co_name)

    ### COPIE ESSA ESTRUTURA PARA A QUANTIDADE DE ETAPAS QUE A AUTOMAÇÃO TERÁ
    @logger_agent.call_log
    def task(self):
        ### LÓGICA DA TASK ###
        ######################

        dao_agent.save_condition(CONDITION_1)
        dao_agent.save_state(inspect.currentframe().f_code.co_name)


def main():
    bot = Bot()
    

if __name__ == "__main__":
    main()
    