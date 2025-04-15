import sqlite3

class Dao():
    def __init__(self):
        self.db = sqlite3.connect('local_db.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def create_custom_process_table(self, methods_list):
        TABLE = "process"
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
        ''')
        for method in methods_list:
            try:
                self.cursor.execute(f'''
                    ALTER TABLE {TABLE} ADD COLUMN {method} BOOLEAN DEFAULT 0
                ''')
            except sqlite3.OperationalError as e:
                if f'duplicate column name: {method}' in str(e).lower():
                    pass  # Ignora se a coluna já existe
                else:
                    raise e
        self.cursor.execute(f'''
            INSERT INTO {TABLE} ({methods_list[0]})
            VALUES (0)
        ''')
        self.db.commit()
        self.last_id = self.cursor.lastrowid

    def create_custom_condition_table(self, condition_list: list):
        TABLE = "conditions"
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lastupdate TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                execution_date DATETIME,
                input INT
            )
        ''')

        for condition in condition_list:
            if condition == "":
                continue
            try:
                self.cursor.execute(f'''
                    ALTER TABLE {TABLE} ADD COLUMN {condition} BOOLEAN DEFAULT 0
                ''')
            except sqlite3.OperationalError as e:
                if f'duplicate column name: {condition}' in str(e).lower():
                    pass  # Ignora se a coluna já existe
                else:
                    raise e
                
        self.cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS index_execution_date ON {TABLE} (execution_date);")
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO {TABLE} (execution_date)
            VALUES (strftime('%Y-%m-%d', 'now', 'localtime'))
        ''')
        self.db.commit()

    def save_state(self, method):
        statement = f'''
            UPDATE process
            SET {method} = ?
            WHERE id = ?
        '''
        self.cursor.execute(statement, (1, self.last_id))
        self.db.commit()
    
    def check_condition(self):
        statement = f'''
            SELECT * FROM conditions
            WHERE DATE(execution_date) = DATE('now', 'localtime')
        '''
        response = self.cursor.execute(statement).fetchone()
        return response
    
    def save_condition(self, CONDITION):
        if CONDITION == "":
            return "No Condition"
        
        self.cursor.execute(
            f"""UPDATE conditions SET {CONDITION} = 1
            WHERE execution_date = strftime('%Y-%m-%d', 'now', 'localtime')"""
        )
        print(self.cursor.rowcount)
        self.db.commit()