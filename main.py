import flask
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime


# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets']

credentials = ServiceAccountCredentials.from_json_keyfile_name("grlproject-credentials.json", scope)
client = gspread.authorize(credentials)

# # Mappings
# Status >> Status sheet \
# rules >> sheet with rules \
# logs_curr >> sheet with logs of curr_year \
# to_do >> todo list (without points) sheet \
# recurring_tasks >> recurring task list (with points)

class GRL:
    def __init__(self):
        self.db_key = "1x8diys3T1XIgbUai197Idpi_sJMhRchDFc-6sFF7fNY"
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

        self.add_log = []
        
    
    # handles failed attempts to write in sheets database
    def repair(self) :
        old_log_count = int(self.sheets['Status'].acell('F2').value)
        new_log_count = int(self.sheets['logs'].acell('A1').value)
        if old_log_count == new_log_count : return
        
        add_log = self.sheets['logs'].get('A{}:A{}'.format(old_log_count + 2, new_log_count + 2))
        for log in add_log :
            operation = log.split(';')[0]
            if operation == "UPDATE SCORE" :
                self.sheets['Status'].update('A2', int(log.split(';')[-1]))
            elif self.dt1_done == 0 and operation == 'COMPLETED DT1' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 1)
            elif self.dt2_done == 0 and operation == 'COMPLETED DT2' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 2)
            elif self.dt3_done == 0 and operation == 'COMPLETED DT3' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 4)
            elif self.dt1_done == 1 and operation == 'UNDO DT1' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 1)
            elif self.dt2_done == 1 and operation == 'UNDO DT2' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 2)
            elif self.dt3_done == 1 and operation == 'UNDO DT3' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 4)
        
        self.sheets['Status'].update('G2', datetime.datetime.strftime(datetime.date.today(), "%Y%m%d"))
        
        self.sheets['Status'].update('F2', new_log_count)
    
    
    # updates sheets database with current changes and logs
    def push_status(self) :
        self.repair()
        
        if len(self.add_log) == 0 : return
        
        cell_ptr = int(self.sheets['logs'].acell('A1').value) + 2
        self.sheets['logs'].update('A{}:A{}'.format(cell_ptr, cell_ptr + len(self.add_log)), [[log] for log in self.add_log])
        self.sheets['logs'].update('A1', cell_ptr + len(self.add_log) - 2)
        
        for log in self.add_log :
            operation = log.split(';')[0]
            if operation == "UPDATE SCORE" :
                self.sheets['Status'].update('A2', int(log.split(';')[-1]))
            elif self.dt1_done == 0 and operation == 'COMPLETED DT1' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 1)
            elif self.dt2_done == 0 and operation == 'COMPLETED DT2' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 2)
            elif self.dt3_done == 0 and operation == 'COMPLETED DT3' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) + 4)
            elif self.dt1_done == 1 and operation == 'UNDO DT1' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 1)
            elif self.dt2_done == 1 and operation == 'UNDO DT2' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 2)
            elif self.dt3_done == 1 and operation == 'UNDO DT3' : 
                self.sheets['Status'].update('E2', int(self.sheets['Status'].acell('E2').value) - 4)
        
        self.sheets['Status'].update('G2', datetime.datetime.strftime(datetime.date.today(), "%Y%m%d"))
            
        self.sheets['Status'].update('F2', cell_ptr + len(self.add_log) - 2)
        
        self.add_log = []
        
    
    @property
    def score(self) :
        return int(self.sheets['Status'].acell('A2').value)
    
    
    @property
    def membership(self) :
        if self.score < 1e6 : return 'D'
        elif self.score < 1e9 : return 'C'
        elif self.score < 1e12 : return 'B'
        elif self.score < 1e15 : return 'A'
        else : return 'S'
    
    
    @property
    def dt1(self) :
        return self.sheets['Status'].acell('B2').value
    
    @property
    def dt2(self) :
        return self.sheets['Status'].acell('C2').value
    
    @property
    def dt3(self) :
        return self.sheets['Status'].acell('D2').value
    
    
    @property
    def dt1_done(self) :
        return (int(self.sheets['Status'].acell('E2').value) % 2)
    
    @dt1_done.setter
    def dt1_done(self, value) :
        if player.dt1_done == value : return
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
    def dt2_done(self) :
        return (int(self.sheets['Status'].acell('E2').value) % 4) // 2
    
    @dt2_done.setter
    def dt2_done(self, value) :
        if player.dt2_done == value : return
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
    def dt3_done(self) :
        return (int(self.sheets['Status'].acell('E2').value) // 4)
    
    @dt3_done.setter
    def dt3_done(self, value) :
        if player.dt3_done == value : return
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
    
    
    
    # not a property because in future we may have it like top 10 or 5 only, also updates will be complicated
    def get_to_do_list(self) :
        return self.sheets['to_do'].col_values(1)
    
    # not a property because in future we may have it like top 10 or 5 only, also updates will be complicated
    def get_recurring_tasks(self) :
        tasks = self.sheets['recurring_tasks'].col_values(1)
        points = self.sheets['recurring_tasks'].col_values(2)
        return dict(zip(tasks, points))

player = GRL() 

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if 'DT_B1' in flask.request.form : player.dt1_done = 1 - player.dt1_done
    if 'DT_B2' in flask.request.form : player.dt2_done = 1 - player.dt2_done
    if 'DT_B3' in flask.request.form : player.dt3_done = 1 - player.dt3_done

    variables = {'score' : player.score,
                 'membership' : player.membership,
                 'DT1' : player.dt1,
                 'DT2' : player.dt2,
                 'DT3' : player.dt3,
                 'DT1_done' : player.dt1_done,
                 'DT2_done' : player.dt2_done,
                 'DT3_done' : player.dt3_done,
                 'to_do' : player.get_to_do_list(),
                 'recurring_tasks' : player.get_recurring_tasks()}
    
    return flask.render_template("index.html", **variables)

if __name__ == '__main__' : app.run()



