## Connecting Backend
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import deque
import datetime
import time
from . import sheets_db_key 
import os

class BackendWriter:
    def __init__(self):
        
        # Connect to Google Sheets
        scope = ['https://www.googleapis.com/auth/spreadsheets']

        DIRNAME = os.path.dirname(__file__)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(DIRNAME, "grlproject-credentials.json"), scope)

        client = gspread.authorize(credentials)
        self.db_wb = client.open_by_key(sheets_db_key)
        
        # initallizing some constants and sheets access in local variables
        curr_year = (datetime.date.today().year) % 100
        self.sheets_name = {"Status" : "Status", 
                            "logs" : "logs {}".format(curr_year), 
                            "rules" : "rules",
                            "to_do" : "to do",
                            'RT' : "recurring"}

        self.sheets = dict([])
        for key, name in self.sheets_name.items() : 
            self.sheets[key] = self.db_wb.worksheet(name)

        # add_log is used to temporarily save logs before pushing them to sheets_db
        self.add_log = []
        
        # deque to keep track of api limits
        self.read_api_calls = deque()
        self.write_api_calls = deque()
        
    
    # keeps track of read calls of sheets api
    def read_api(self) : 
        self.read_api_calls.append(time.time())
        while len(self.read_api_calls) > 50 : 
            while (self.read_api_calls[0] + 60) < time.time() : self.read_api_calls.popleft()
            print('read_limit')
            time.sleep(2)

    # keeps track of write calls of sheets api
    def write_api(self) : 
        self.write_api_calls.append(time.time())
        while len(self.write_api_calls) > 50 : 
            while (self.write_api_calls[0] + 60) < time.time() : self.write_api_calls.popleft()
            print('write_limit')
            time.sleep(2)


    # stores info on score related updates
    @staticmethod
    def add_score(updates, log) :
        updates['Status'].append({'range' : 'A2', 'values' : [[int(log.split(';')[-1])]]})
        
    # stores info on dt_completed related updates
    @staticmethod
    def add_dt_completed(updates, log, t, v) :
        task_no = '$EFG'
        updates['Status'].append({'range' : '{}2'.format(task_no[t]), 'values' : [[v]]})
        
    # stores info on 'last time of update' in updates
    @staticmethod
    def add_time_update(updates) :
        updates['Status'].append({'range' : 'I2', 'values' : [[datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")]]})
        
    # stores info on 'td_completed' in updates
    @staticmethod
    def add_td_completed(updates, log, t, v, score_diff = 0) :
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        if v == 1 : updates['to_do'].append({'range' : 'B{}:C{}'.format(int(t) + 1, int(t) + 1), 'values' : [[_today, score_diff]]})
        else : updates['to_do'].append({'range' : 'B{}'.format(int(t) + 1), 'values' : [[-1]]})

    # stores info on 'rt_completed' in updates
    @staticmethod
    def add_rt_completed(updates, log, t, v) :
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        _before = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days = 1), "%Y%m%d")
        
        if v == 1 : updates['RT'].append({'range' : 'C{}'.format(int(t) + 1), 'values' : [[_today]]})
        else : updates['RT'].append({'range' : 'C{}'.format(int(t) + 1), 'values' : [[_before]]})
    
    # stores info on 'td_add' in updates
    @staticmethod
    def add_td(updates, log, t) :
        l = updates['variables'].get('to_do_l') + 1
        updates['variables']['to_do_l'] = l
        updates['to_do'].append({'range' : 'A{}:B{}'.format(l, l), 'values' : [[t, -1]]})
        
    # stores info on 'rt_add' in updates
    @staticmethod
    def add_rt(updates, log, t, pts) :
        l = updates['variables'].get('RT_l') + 1
        updates['variables']['RT_l'] = l
        updates['RT'].append({'range' : 'A{}:C{}'.format(l, l), 'values' : [[t, pts, 0]]})
        
    # replaces DT with 'Add Daily Task' at end of day
    @staticmethod
    def reset_dt(updates) :
        updates['Status'].append({'range' : 'B2:G2', 'values' : [['Add Daily Task', 'Add Daily Task', 'Add Daily Task', 0, 0, 0]]})
    
    # Creates DT
    @staticmethod
    def add_DT_Create(updates, log) :
        _cellA = {'1' : 'B2', '2' : 'C2', '3' : 'D2'}
        updates['Status'].append({'range' : _cellA[log.split(';')[1]], 'values' : [[log.split(';')[-1]]]})
        
    # updates last score in status sheet in updates
    @staticmethod
    def add_last_score(updates, log, score) :
        updates['Status'].append({'range' : 'J2', 'values' : [[int(score)]]})
        
    # updates task edited by user in updates
    @staticmethod
    def add_td_update(updates, log, t_no, new_task) :
        updates['to_do'].append({'range' : f'A{t_no + 1}', 'values' : [[new_task]]})
        
    # updates task edited by user in updates
    @staticmethod
    def add_rt_update(updates, log, t_no, new_task, new_point) :
        updates['RT'].append({'range' : f'A{t_no + 1}:B{t_no + 1}', 'values' : [[new_task, new_point]]})
    
    # pushes all stored updates together so that api calls needed are less
    def push_all_updates(self, updates) :
        for sheet, update_list in updates.items() :
            if sheet == 'variables' : continue
            if len(update_list) == 0 : continue
            self.sheets[sheet].batch_update(update_list)
            self.write_api()
    
    
    # helper function to process log and call appropriate add functions
    def process_log(self, log, updates) :
        operation = log.split(';')[0]
        if operation == "UPDATE SCORE" :
            self.add_score(updates, log)
        elif operation == 'DT_Create' :
            self.add_DT_Create(updates, log)
        elif operation == 'COMPLETED DT1' :
            self.add_dt_completed(updates, log, 1, 1)
        elif operation == 'COMPLETED DT2' : 
            self.add_dt_completed(updates, log, 2, 1)
        elif operation == 'COMPLETED DT3' : 
            self.add_dt_completed(updates, log, 3, 1)
        elif operation == 'UNDO DT1' :
            self.add_dt_completed(updates, log, 1, 0)
        elif operation == 'UNDO DT2' : 
            self.add_dt_completed(updates, log, 2, 0)
        elif operation == 'UNDO DT3' : 
            self.add_dt_completed(updates, log, 3, 0)
        elif operation == 'TD_completed' :
            self.add_td_completed(updates, log, log.split(';')[1], 1, int(log.split(';')[3]))
        elif operation == 'TD_UNDO' :
            self.add_td_completed(updates, log, log.split(';')[1], 0)
        elif operation == 'RT_completed' :
            self.add_rt_completed(updates, log, log.split(';')[1], 1)
        elif operation == 'RT_UNDO' :
            self.add_rt_completed(updates, log, log.split(';')[1], 0)
        elif operation == 'NEW DAY' :
            self.add_time_update(updates)
        elif operation == 'TD_ADD' :
            self.add_td(updates, log, log.split(';')[1])
        elif operation == 'RT_ADD' :
            self.add_rt(updates, log, log.split(';')[1], log.split(';')[2])
        elif operation == 'TD_DEL' :
            self.read_api()
            if self.sheets['to_do'].acell('A{}'.format(int(log.split(';')[1]) + 1)).value != log.split(';')[2] : return
            self.sheets['to_do'].delete_rows(int(log.split(';')[1]) + 1)
            self.write_api()
        elif operation == 'RT_DEL' :
            self.read_api()
            if self.sheets['RT'].acell('A{}'.format(int(log.split(';')[1]) + 1)).value != log.split(';')[2] : return
            self.sheets['RT'].delete_rows(int(log.split(';')[1]) + 1)
            self.write_api()
        elif operation == 'RESET_DT' :
            self.reset_dt(updates)
        elif operation == 'LAST SCORE' :
            self.add_last_score(updates, log, log.split(';')[1])
        elif operation == 'TD_UPDATE' :
            self.add_td_update(updates, log, int(log.split(';')[1]), log.split(';')[3])
        elif operation == 'RT_UPDATE' :
            self.add_rt_update(updates, log, int(log.split(';')[1]), log.split(';')[3], int(log.split(';')[4]))


    # handles failed attempts to write in sheets db
    def repair_sheet(self) :
        old_log_count = int(self.sheets['Status'].acell('H2').value)
        new_log_count = int(self.sheets['logs'].acell('A1').value)
        self.read_api()
        self.read_api()
        if old_log_count == new_log_count : return
        
        temp_add_log = self.sheets['logs'].get('A{}:A{}'.format(old_log_count + 2, new_log_count + 2))
        self.read_api()
        
        updates = {key : [] for key in self.sheets.keys()}
        
        # it is created to store things like length of to do list because 
        updates['variables'] = dict({})            
        
        for log in temp_add_log[0] :
            self.process_log(log, updates)
        
        self.push_all_updates(updates)
        
        self.sheets['Status'].update('H2', new_log_count)     # updating final log count in status sheet
        self.read_api()
        
    
    # updates sheets db with current changes and logs
    def push_status(self) :
        
        if len(self.add_log) == 0 : return       # if there's no log to push, return
        
        # reading position for next empty cell in logs and pushing logs in db and updating count of logs
        cell_ptr = int(self.sheets['logs'].acell('A1').value) + 2
        self.sheets['logs'].update('A{}:A{}'.format(cell_ptr, cell_ptr + len(self.add_log)), [[log] for log in self.add_log])
        self.sheets['logs'].update('A1', cell_ptr + len(self.add_log) - 2)
        
        self.read_api()                     # tracking api calls
        self.write_api()
        self.write_api()
        
        updates = {key : [] for key in self.sheets.keys()}
        updates['variables'] = dict({})
        updates['variables']['to_do_l'] = self.TD_l
        updates['variables']['RT_l'] = self.RT_l
        
        for log in self.add_log :
            self.process_log(log, updates)
        
        self.push_all_updates(updates)
        
        self.sheets['Status'].update('H2', cell_ptr + len(self.add_log) - 2)     # updating final log count in status sheet
        self.read_api()

        self.add_log = []
    

    # pulls status from db in as it is form in dictionary
    # necessary formatting of variables is performed while accessing variable by getters or equivalent functions  
    def pull_status(self) :
        self.repair_sheet()
        zipped_temp_sheet = zip(*self.sheets['Status'].get_values())
        self.read_api()
        variables = dict({})
        
        for key, value in zipped_temp_sheet :
            variables[key] =  value 
        
        variables['to_do'] = self.sheets['to_do'].get_values()
        variables['RT'] = self.sheets['RT'].get_values()
        self.read_api()
        self.read_api()
        
        self.TD_l = len(variables['to_do'])
        self.RT_l = len(variables['RT'])
        ################### fetched 4 sheets till now need to see what is needed as per update functions ###############
    
        return variables
        