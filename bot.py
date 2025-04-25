from logger import Logger
from dao import Dao
import inspect
import os
from colorama import Fore, Back, Style, ansi

### OUTRAS IMPORTAÇÕES
import openpyxl
###

print(ansi.clear_screen())
print(ansi.set_title("Prompt Bot - Modelo"))

logger_agent = Logger(file_level=0, stream_level=10)
dao_agent = Dao()

CONDITION_1 = ""
CONDITION_2 = ""
CONDITION_3 = ""
CONDITION_99 = ""

class Bot():
    @logger_agent.call_log
    def __init__(self):
        print(f"{Fore.LIGHTMAGENTA_EX}Bot Instancializado\nCWD: {os.getcwd()}\nMétodos:{Style.RESET_ALL}")
        methods_list = [method for method in Bot.__dict__.keys() if not method.startswith("__")]
        for key in methods_list:
            print(f"{Fore.LIGHTMAGENTA_EX}    =>", key,Style.RESET_ALL)

        condition_list = [CONDITION_1, CONDITION_2, CONDITION_3]

        dao_agent.create_custom_process_table(methods_list)
        dao_agent.create_custom_condition_table(condition_list)

    ### COPIE ESSA ESTRUTURA PARA A QUANTIDADE DE ETAPAS QUE A AUTOMAÇÃO TERÁ
    ########################################################################################
    ########################################################################################
    @logger_agent.call_log
    def __task_1__(self):
        if dao_agent.check_condition(CONDITION_99) not in (None, False): logger_agent.logger.info(f"{inspect.currentframe().f_code.co_name} - CHECADO"); return True
        print("EXECUTANDO TASK 1")
        ### LÓGICA DA TASK ###
        ...
        ######################
        dao_agent.save_condition(CONDITION_99); dao_agent.save_state(inspect.currentframe().f_code.co_name)
    ########################################################################################
    ########################################################################################


    @logger_agent.call_log
    def task_crawler(self):
        CONDITION = CONDITION_1
        if dao_agent.check_condition(CONDITION) not in (None, False): logger_agent.logger.info(f"{inspect.currentframe().f_code.co_name} - CHECADO"); return True
        logger_agent.logger.info("EXECUTANDO TASK CRAWLER")
        ### LÓGICA DA TASK ###
        from crawler import main_crawler
        main_crawler()
        ######################
        dao_agent.save_condition(CONDITION); dao_agent.save_state(inspect.currentframe().f_code.co_name)
    
    @logger_agent.call_log
    def task_xlsx(self):
        CONDITION = CONDITION_2
        if dao_agent.check_condition(CONDITION) not in (None, False): logger_agent.logger.info(f"{inspect.currentframe().f_code.co_name} - CHECADO"); return True
        logger_agent.logger.info("EXECUTANDO TASK XLSX")
        ### LÓGICA DA TASK ###
        from manager_excel import main_excel
        main_excel()
        ######################
        dao_agent.save_condition(CONDITION); dao_agent.save_state(inspect.currentframe().f_code.co_name)

    @logger_agent.call_log
    def task_slack(self):
        CONDITION = CONDITION_99
        if dao_agent.check_condition(CONDITION) not in (None, False): logger_agent.logger.info(f"{inspect.currentframe().f_code.co_name} - CHECADO"); return True
        logger_agent.logger.info("EXECUTANDO TASK SLACK")
        ### LÓGICA DA TASK ###
        ...
        ######################
        dao_agent.save_condition(CONDITION); dao_agent.save_state(inspect.currentframe().f_code.co_name)

def main():
    bot = Bot()
    bot.task_crawler()
    bot.task_xlsx()
    bot.task_slack()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logger_agent.logger.warning(f"Ocorreu um erro muito sério! - {error}") ### Envio de email para nível CRITICAL

