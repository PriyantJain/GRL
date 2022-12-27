import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time
from collections import deque


class GRL:
    def __init__(self):
        # Connect to Google Sheets
        scope = ['https://www.googleapis.com/auth/spreadsheets']

        credentials = ServiceAccountCredentials.from_json_keyfile_name("grlproject-credentials.json", scope)
        client = gspread.authorize(credentials)

        # initallizing some constants and sheets access in local variables
        self.db_key = "11glFKrtVXULhoUB5h4LgQOoJlt3ckuCaI4SRX_E-eng"
        self.db_wb = client.open_by_key(self.db_key)

        curr_year = (datetime.date.today().year) % 100
        self.sheets_name = {"Status" : "Status", 
                            "logs" : "logs {}".format(curr_year), 
                            "rules" : "rules",
                            "to_do" : "to do",
                            'recurring_tasks' : "recurring"}

        self.sheets = dict([])
        for key, name in self.sheets_name.items() : 
            self.sheets[key] = self.db_wb.worksheet(name)

        # add_log is used to temporarily save logs before pushing them to sheets_db
        self.add_log = []
        
        # deque to keep track of api limits
        self.read_api_calls = deque()
        self.write_api_calls = deque()
        
        self.variables = dict({})
        
        ########### initial status pull needs to decide if same pull_status or not #################
        self.pull_status()
        self.new_day()
        
    # keeps track of read calls of sheets api
    def read_api(self) : 
        self.read_api_calls.append(time.time())
        while len(self.read_api_calls) > 50 : 
            while (self.read_api_calls[0] + 1) < time.time() : self.read_api_calls.popleft()
            print('read_limit')
            time.sleep(2)

    # keeps track of write calls of sheets api
    def write_api(self) : 
        self.write_api_calls.append(time.time())
        while len(self.write_api_calls) > 50 : 
            while (self.write_api_calls[0] + 1) < time.time() : self.write_api_calls.popleft()
            print('write_limit')
            time.sleep(2)


    # stores info on score related updates
    def add_score(self, updates, log) :
        updates['Status'].append({'range' : 'A2', 'values' : [[int(log.split(';')[-1])]]})
        
    # stores info on dt_completed related updates
    def add_dt_completed(self, updates, log, t, v) :
        task_no = '$EFG'
        updates['Status'].append({'range' : '{}2'.format(task_no[t]), 'values' : [[v]]})
        
    # stores info on 'last time of update' in updates
    def add_time_update(self, updates) :
        updates['Status'].append({'range' : 'I2', 'values' : [[datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")]]})
        
        
    # pushes all stored updates together so that api calls needed are less
    def push_all_updates(self, updates) :
        for sheet, update_list in updates.items() :
            if len(update_list) == 0 : continue
            self.sheets[sheet].batch_update(update_list)
            self.write_api()
    
    
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
        for log in temp_add_log[0] :
            operation = log.split(';')[0]
            if operation == "UPDATE SCORE" :
                self.add_score(updates, log)
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
        
        ############# is it needed here????? ##########
        self.add_time_update(updates)    # updating last open date
        
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
        
        for log in self.add_log :
            operation = log.split(';')[0]
            if operation == "UPDATE SCORE" :
                self.add_score(updates, log)
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
        
        
        ############# is it needed here????? ##########
        self.add_time_update(updates)    # updating last open date
        
        self.push_all_updates(updates)
        
        self.sheets['Status'].update('H2', cell_ptr + len(self.add_log) - 2)     # updating final log count in status sheet
        self.read_api()
        
        self.add_log = []
        self.pull_status()
    
    
    # pulls status from db in as it is form in dictionary
    # necessary changes are performed in accessing variable from '.' operator  
    def pull_status(self) :
        self.repair_sheet()
        zipped_temp_sheet = zip(*self.sheets['Status'].get_values())
        self.read_api()
        
        for key, value in zipped_temp_sheet :
            self.variables[key] =  value 
        
        self.variables['to_do'] = self.sheets['to_do'].get_values()
        self.variables['recurring_tasks'] = self.sheets['recurring_tasks'].get_values()
        ################### fetched 4 sheets till now need to see what is needed as per update functions ###############
    
    
    ############# need to complete new_day feature #####################
    # checks whether new day and performs daily tasks
    def new_day(self) :
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        if self.variables['Last open'] == _today : return
        
        daily_charge = {'S' : 500, 'A' : 700, 'B' : 800, 'C' : 900, 'D' : 1000}
        
        self.add_log = ['NEW DAY;' + _today + ';DAILY CHARGE;']
        old_score = self.score
        new_score = self.score
        new_score -= daily_charge[self.membership]
#         self.add_log.append('RESET DT;')
        self.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.push_status()
    
    @property
    def score(self) :
        return int(self.variables['Score'])
    
    @property
    def membership(self) :
        if self.score < 1e6 : return 'D'
        elif self.score < 1e9 : return 'C'
        elif self.score < 1e12 : return 'B'
        elif self.score < 1e15 : return 'A'
        else : return 'S'
    
    
    
    @property
    def dt1(self) :    return self.variables['DT1']
    
    @property
    def dt2(self) :    return self.variables['DT2']
    
    @property
    def dt3(self) :    return self.variables['DT3']
    
    
    
    @property
    def dt1_done(self) :    return int(self.variables['DT1_completed'])
    
    @dt1_done.setter
    def dt1_done(self, value) :
        if self.dt1_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.add_log = ["COMPLETED DT1;" + self.dt1 + ";"]
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.add_log = ["UNDO DT1;" + self.dt1 + ";"]
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.push_status()
         
    @property
    def dt2_done(self) :    return int(self.variables['DT2_completed'])
    
    @dt2_done.setter
    def dt2_done(self, value) :
        if self.dt2_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.add_log = ["COMPLETED DT2;" + self.dt2 + ";"]
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.add_log = ["UNDO DT2;" + self.dt2 + ";"]
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.push_status()
    
    @property
    def dt3_done(self) :    return int(self.variables['DT3_completed'])
    
    @dt3_done.setter
    def dt3_done(self, value) :
        if self.dt3_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.add_log = ["COMPLETED DT3;" + self.dt3 + ";"]
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.add_log = ["UNDO DT3;" + self.dt3 + ";"]
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.push_status()
    
    def get_to_do_list(self) :
        return [task for task, done in dict(self.variables['to_do']).items() if done == '-1']
    
    def get_recurring_tasks(self) :
        return {task : val for task, *val in self.variables['recurring_tasks']}