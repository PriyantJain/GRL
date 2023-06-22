import MySQLdb
from . import host, user, password, database

class BackendWriter:
    def __init__(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = MySQLdb.connect(host=host, user=user, password=password, database=database)
        self.tables = ['STATS', 'TO_DO_TASKS', 'RECURRING_TASKS', 'USER_LOGS']
        self.logs = []
        self.queries = []

    def check_connection(self):
        if self.connection.open == 1 : self.connection.close()
        self.connection = MySQLdb.connect(host=host, user=user, password=password, database=database)

    def update_score(self, old_score, new_score) : self.queries.append(f'''UPDATE STATS SET Score = '{new_score}' WHERE Id = 1;''')

    def update_last_open_date(self, _today) : self.queries.append(f'''UPDATE STATS SET Last_Open = '{_today}' WHERE Id = 1;''')

    def update_last_day_score(self, last_score) : self.queries.append(f'''UPDATE STATS SET Last_Day_Score = '{last_score}' WHERE Id = 1;''')

    def add_daily_task(self, t_no, task) :    self.queries.append(f'''UPDATE STATS SET DT_{t_no} = '{task}' WHERE Id = 1;''')

    def delete_daily_task(self, default_message) :
        self.queries.append(f'''UPDATE STATS
                                SET DT_1 = '{default_message}', DT_2 = '{default_message}', DT_3 = '{default_message}',
                                DT_1_completed = 0, DT_2_completed = 0, DT_3_completed = 0
                                WHERE Id = 1;''')

    def toggle_dt(self, t_no, state) :  self.queries.append(f'''UPDATE STATS SET DT_{t_no}_completed = '{state}' WHERE Id = 1;''')

    def add_to_do(self, task, parent = '-1') : 
        
        self.queries.append(f'''INSERT INTO TO_DO_LIST(Task_Name, Parent) VALUES('{task}', {parent});''')
        if parent == '-1' :
            self.queries.append('''UPDATE TO_DO_LIST
                                    SET Parent = (SELECT * FROM (SELECT MAX(Sr_No) FROM TO_DO_LIST) TEMPTB )
                                    WHERE Sr_No = (SELECT * FROM (SELECT MAX(Sr_No) FROM TO_DO_LIST) TEMPTB1 );
                                ''')

    def complete_to_do(self, t_no, _today, points) :
        self.queries.append(f"""INSERT INTO TO_DO_COMPLETED (Sr_No, Task_Name, Track, Parent, Task_Points, Completion_Date) 
                                SELECT Sr_No, Task_Name, Track, Parent, '{points}', '{_today}' FROM TO_DO_LIST WHERE Sr_No = {t_no};""")
        self.queries.append(f"""DELETE FROM TO_DO_LIST WHERE Sr_No = {t_no};""")

    def undo_to_do(self, t_no) :
        self.queries.append(f'''INSERT INTO TO_DO_LIST (Sr_No, Task_Name, Track, Parent) SELECT Sr_No, Task_Name, Track, Parent FROM TO_DO_COMPLETED WHERE Sr_No = {t_no};''')
        self.queries.append(f'''DELETE FROM TO_DO_COMPLETED WHERE Sr_No = {t_no};''')

    def delete_to_do(self, t_no) :    self.queries.append(f'''DELETE FROM TO_DO_LIST WHERE Sr_No = {t_no};''')

    def update_to_do(self, t_no, new_name, new_track) :
        self.queries.append(f'''UPDATE TO_DO_LIST SET Task_Name = '{new_name}', Track = '{new_track}' WHERE Sr_No = {t_no};''')

    def add_recurring_task(self, task, pts) :
        self.queries.append(f'''INSERT INTO RECURRING_TASKS(Task_Name, Last_Completion_Date, Task_Points) VALUES('{task}', '0', '{pts}');''')

    def complete_recurring_task(self, t_no, _today) :
        self.queries.append(f'''UPDATE RECURRING_TASKS SET Last_Completion_Date = '{_today}' WHERE Sr_No = {t_no};''')

    def undo_recurring_task(self, t_no) :
        self.queries.append(f'''UPDATE RECURRING_TASKS SET Last_Completion_Date = '0' WHERE Sr_No = {t_no};''')

    def delete_recurring_task(self, t_no) :    self.queries.append(f'''DELETE FROM RECURRING_TASKS WHERE Sr_No = {t_no};''')

    def update_recurring_task(self, t_no, new_name, new_pts) :
        self.queries.append(f'''UPDATE RECURRING_TASKS SET Task_Name = '{new_name}', Task_Points = '{new_pts}' WHERE Sr_No = {t_no};''')

    def commit(self) :
        if len(self.add_log) == 0 : return       # if there's no log to push, return

        self.check_connection()
        self.connection.begin()
        cursor = self.connection.cursor()

        try :
            cursor.executemany('''INSERT INTO USER_LOGS(Log) Values(%s)''', [(log,) for log in self.add_log])
            for query in self.queries : cursor.execute(query)
            self.queries = []
            self.connection.commit()
        except MySQLdb.Error as e :
            print(f"Error: {e}")
            self.queries = []
            self.connection.rollback()
            raise


    def get_table_data(self, table_name) :
        self.check_connection()
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        col_names = tuple(desc[0] for desc in cursor.description)
        return (col_names, *cursor.fetchall())

    # def get_tree_list(self, child_of, root) :
    #     tree = [[root, min(1, len(child_of.get(root, [])))]]    # 1 means node has children
    #     for child in child_of.get(root, []) :
    #         tree.extend(self.get_tree_list(child_of, child))
    #     return tree

    def pull_status(self, _today):
        variables = dict([])

        for col, val in zip(*self.get_table_data('STATS')) :    variables[col] = val

        to_do_list = self.get_table_data('TO_DO_LIST')
        child_of = dict([])
        roots = []

        for to_do in to_do_list :
            if to_do[3] not in child_of.keys() : child_of[to_do[3]] = []
            if to_do[3] == to_do[0] : 
                roots.append(to_do[0])
                continue
            child_of[to_do[3]].append(to_do[0])

        variables['to_do'] = {row[0] : row[1:] for row in to_do_list}
        variables['to_do_list'] = []
        # for root in roots : variables['to_do_list'].extend(self.get_tree_list(child_of, root))
        for root in roots : variables['to_do_list'].append([root] + child_of[root])
        
        variables['to_do_completed'] = {row[0] : row[1:] for row in self.get_table_data('TO_DO_COMPLETED')}

        variables['RT'] = {row[0] : row[1:] for row in self.get_table_data('RECURRING_TASKS') if row[2] != _today}
        variables['RT_completed'] = {row[0] : row[1:] for row in self.get_table_data('RECURRING_TASKS') if row[2] == _today}

        return variables

    def __del__(self):
        print('Closing connection via __del__ ...')
        self.connection.close()
