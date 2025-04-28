# model-bot-logging-db

Este projeto é um modelo de bot que utiliza logging avançado e persistência de dados em um banco SQLite. Ele foi projetado para executar tarefas automatizadas com controle de condições e etapas, além de oferecer suporte a notificações via e-mail em caso de erros críticos.

## Funcionalidades

- **Logging Avançado**: Logs detalhados com níveis configuráveis (arquivo, console, e-mail).
- **Persistência de Dados**: Uso de SQLite para armazenar estados e condições de execução.
- **Automação de Tarefas**: Estrutura modular para adicionar e gerenciar tarefas automatizadas.
- **Notificações**: Integração com e-mail para alertas críticos.

## Estrutura do Projeto
- **.env** # Variáveis de ambiente (ex.: credenciais de e-mail)
- **.gitignore** # Arquivos e pastas ignorados pelo Git
- **bot.py** # Lógica principal do bot
- **dao.py** # Classe para interação com o banco de dados SQLite
- **logger.py** # Classe para configuração e gerenciamento de logs
- **local_db.db** # Banco de dados SQLite local
- **logs.log** # Arquivo de logs gerado durante a execução
- **LICENSE** # Licença do projeto (MIT)
- **README.md** # Documentação do projeto

## Pré-requisitos

- Python 3.10 ou superior
- Biblioteca `sqlite3` (inclusa no Python)
- Dependências adicionais (instaladas via `pip`):
  - `colorama`
  - `python-dotenv`
  
## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/model-bot-logging-db.git
   cd model-bot-logging-db

2. Crie e configure o arquivo .env:
APP_PASSWORD="sua-senha-de-aplicativo"

3. Instale as dependências:
pip install -r requirements.txt

4. Certifique-se de que o banco de dados SQLite (local_db.db) está no diretório raiz do projeto.

Uso
1. Execute o bot:
python bot.py

2. O bot executará as tarefas definidas em bot.py, verificando condições e salvando estados no banco de dados.

3. Logs serão gerados no console e no arquivo logs.log. Em caso de erros críticos, notificações serão enviadas por e-mail e Slack (se configurados).

Estrutura de Tarefas
As tarefas são definidas como métodos na classe Bot em bot.py. Cada tarefa segue a estrutura:
```bash
@logger_agent.call_log
def task_nome(self):
    CONDITION = "nome_da_condicao"
    if dao_agent.check_condition(CONDITION) not in (None, False):
        logger_agent.logger.info(f"{inspect.currentframe().f_code.co_name} - CHECADO")
        return True
    print("EXECUTANDO TASK NOME")
    # Lógica da tarefa
    ...
    dao_agent.save_condition(CONDITION)
    dao_agent.save_state(inspect.currentframe().f_code.co_name)
```
Personalização
Adicionar Tarefas: Crie novos métodos na classe Bot e adicione condições personalizadas.
Configurar Logging: Ajuste os níveis de log no arquivo logger.py.
Banco de Dados: Modifique a estrutura das tabelas no arquivo dao.py.
Licença
Este projeto está licenciado sob a Licença MIT.

Autor
Desenvolvido por Sanzio Dinelli.
Este [README.md](http://_vscodecontentref_/7) fornece uma visão geral do projeto, instruções de configuração e uso, além de detalhes sobre como personalizar e expandir o bot.