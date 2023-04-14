import datetime
import time
import random
from ..model.mysql_writer import BackendWriter

class GRL_class:
    def __init__(self):
        #creating backend object
        self.db = BackendWriter()
        
        # self variables helps transfer some value easily across class
        self.pull_status()
        self.new_day()
    
    def pull_status(self) :
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        self.variables = self.db.pull_status(_today)
    
    # checks whether new day and performs daily tasks
    def new_day(self) :
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        if self.variables['Last_Open'] == _today : return
        
        daily_charge = {'S' : 500, 'A' : 700, 'B' : 800, 'C' : 900, 'D' : 1000}

        old_score = self.score
        new_score = self.score
        days_missed = datetime.datetime.strptime(_today, '%Y%m%d') - datetime.datetime.strptime(self.variables['Last_Open'], '%Y%m%d')
        new_score -= daily_charge[self.membership] * days_missed.days
        last_score = new_score + daily_charge[self.membership]

        self.db.add_log = ['NEW DAY;' + _today + ';DAILY CHARGE;']
        self.db.update_last_open_date(_today)

        self.db.add_log.append('RESET_DT;') 
        self.db.delete_daily_task('Add Daily Task')

        if self.dt1_done == 0 and self.dt1 != 'Add Daily Task': 
            self.db.add_log.append('TD_ADD;{};'.format(self.dt1))
            self.db.add_to_do(self.dt1)
        if self.dt2_done == 0 and self.dt2 != 'Add Daily Task' : 
            self.db.add_log.append('TD_ADD;{};'.format(self.dt2))
            self.db.add_to_do(self.dt2)
        if self.dt3_done == 0 and self.dt3 != 'Add Daily Task' : 
            self.db.add_log.append('TD_ADD;{};'.format(self.dt3))
            self.db.add_to_do(self.dt3)

        self.db.add_log.append('LAST SCORE;' + str(last_score))
        self.db.update_last_day_score(last_score)

        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)

        self.db.commit()
        self.pull_status()
        
    
    @property
    def score(self) :    return int(self.variables['Score'])
    
    @property
    def membership(self) :
        if self.score < 1e6 : return 'D'
        elif self.score < 1e9 : return 'C'
        elif self.score < 1e12 : return 'B'
        elif self.score < 1e15 : return 'A'
        else : return 'S'
    
    @property
    def today_target(self) :
        return int(int(self.variables['Last_Day_Score']) * (0.9 if int(self.variables['Last_Day_Score']) < 0 else 1.1))
    
        
    def DtCreateSubmit(self, task_no, task):
        if task_no not in list('123') : return
        self.db.add_log = ['DT_Create;{};{}'.format(task_no, task)]
        self.db.add_daily_task(task_no, task)
        self.db.commit()
        self.pull_status()
    
    @property
    def dt1(self) :    return self.variables['DT_1']
    
    @property
    def dt2(self) :    return self.variables['DT_2']
    
    @property
    def dt3(self) :    return self.variables['DT_3']
    
    @property
    def dt1_done(self) :    return int(self.variables['DT_1_completed'])
    
    @dt1_done.setter
    def dt1_done(self, value) :
        if self.dt1_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.db.add_log = ["COMPLETED DT1;" + self.dt1 + ";"]
            self.db.toggle_dt(1, 1)
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.db.add_log = ["UNDO DT1;" + self.dt1 + ";"]
            self.db.toggle_dt(1, 0)
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
        
    @property
    def dt2_done(self) :    return int(self.variables['DT_2_completed'])
    
    @dt2_done.setter
    def dt2_done(self, value) :
        if self.dt2_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.db.add_log = ["COMPLETED DT2;" + self.dt2 + ";"]
            self.db.toggle_dt(2, 1)
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.db.add_log = ["UNDO DT2;" + self.dt2 + ";"]
            self.db.toggle_dt(2, 0)
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
    
    @property
    def dt3_done(self) :    return int(self.variables['DT_3_completed'])
    
    @dt3_done.setter
    def dt3_done(self, value) :
        if self.dt3_done == value : return                     # really needed ?? or needs to be modified ??
        t_done = self.dt1_done + self.dt2_done + self.dt3_done
        old_score = self.score
        new_score = self.score
        
        if value == 1 : 
            self.db.add_log = ["COMPLETED DT3;" + self.dt3 + ";"]
            self.db.toggle_dt(3, 1)
            if t_done == 0 : new_score += 200
            elif t_done == 1 : new_score += 300
            else : new_score += 500
        else :
            self.db.add_log = ["UNDO DT3;" + self.dt3 + ";"]
            self.db.toggle_dt(3, 0)
            if t_done == 1 : new_score -= 200
            elif t_done == 2 : new_score -= 300
            else : new_score -= 500
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
    
    
    def ET(self, task, pt_change) :
        pt_change = int(pt_change)
        self.db.add_log = []
        self.db.add_log.append('ET;{};{};'.format(task, pt_change))
        old_score = self.score
        new_score = self.score + pt_change
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        
        self.db.commit()
        self.pull_status()
        
    def StandardTasksSubmit(self, task, value) :
        if task == 'Select' : return
        
        self.db.add_log = []
        old_score = self.score
        _before = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days = 1), "%Y%m%d")
        value = int(value)
        
        if task == 'Walk' : 
            self.db.add_log.append('WALK;{};{};'.format(_before, value//10))
            new_score = self.score + value // 10  
        elif task == 'Learning' : 
            self.db.add_log.append('Learning;{};'.format(value * 100))
            new_score = self.score + value * 100
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)

        self.db.commit()
        self.pull_status()
        

    def get_to_do_list(self) :    return [(key, *val) for key, val in self.variables['to_do'].items()] 
    def get_to_do_done(self) :    return [(key, *val) for key, val in self.variables['to_do_completed'].items()][1:]

    def TD_add(self, task) : 
        self.db.add_log = []
        self.db.add_log.append('TD_ADD;{};'.format(task))
        self.db.add_to_do(task)
        self.db.commit()
        self.pull_status()
    
    def TD_completed(self, t_no) :    
        # assert t_no in self.variables['to_do'].keys()
        self.db.add_log = []
        old_score = self.score
        new_score = self.score
        max_profit = {'S' : 1e15, 'A' : 1e12, 'B' : 1e9, 'C' : 1e6, 'D' : 1e3}
        
        if (self.dt1_done + self.dt2_done + self.dt3_done) == 3 : 
            new_score += int(random.triangular(50, max_profit[self.membership], 50))
        else : new_score += 50
            
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        self.db.add_log.append('TD_completed;{};{};{};'.format(t_no, self.variables['to_do'][t_no][0], new_score - old_score))
        self.db.complete_to_do(t_no, _today, new_score - old_score)
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
        
    def TD_undo(self, t_no) :    
        # assert self.variables['to_do'][t_no][1] != '-1'
        self.db.add_log = []
        self.db.add_log.append('TD_UNDO;{};{};'.format(t_no, self.variables['to_do_completed'][t_no][0]))
        self.db.undo_to_do(t_no)

        old_score = self.score
        new_score = self.score - int(self.variables['to_do_completed'][t_no][2])
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
        
    def TD_del(self, t_no) :
        self.db.add_log = []
        self.db.add_log.append('TD_DEL;{};{};'.format(t_no, self.variables['to_do'][t_no][0]))
        self.db.delete_to_do(t_no)
        self.db.commit()
        self.pull_status()
        
    def TD_update(self, t_no, new_name) :
        self.db.add_log = []
        self.db.add_log.append('TD_UPDATE;{};{};{};'.format(t_no, self.variables['to_do'][t_no][0], new_name))
        self.db.update_to_do(t_no, new_name)
        self.db.commit()
        self.pull_status()
        
        
    
    def get_RT_list(self) :    return [(key, *val) for key, val in self.variables['RT'].items()][1:]
    def get_RT_done(self) :    return [(key, *val) for key, val in self.variables['RT_completed'].items()]
        
    def RT_add(self, task, pts) : 
        self.db.add_log = []
        self.db.add_log.append('RT_ADD;{};{};'.format(task, pts))
        self.db.add_recurring_task(task, pts)
        self.db.commit()
        self.pull_status()
        
    def RT_completed(self, t_no) :    
        # assert self.variables['RT'][t_no][2] != self.variables['Last_Open']
        self.db.add_log = []
        old_score = self.score
        new_score = self.score + int(self.variables['RT'][t_no][2])
            
        self.db.add_log.append('RT_completed;{};{};'.format(t_no, self.variables['RT'][t_no][0]))
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        self.db.complete_recurring_task(t_no, _today)
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
        
    def RT_undo(self, t_no) :    
        # assert self.variables['RT'][t_no][2] == self.variables['Last_Open']
        self.db.add_log = []
        self.db.add_log.append('RT_UNDO;{};{};'.format(t_no, self.variables['RT_completed'][t_no][0]))
        self.db.undo_recurring_task(t_no)

        old_score = self.score
        new_score = self.score - int(self.variables['RT_completed'][t_no][2])
        
        self.db.add_log.append('UPDATE SCORE;' + str(old_score) + ';' + str(new_score))
        self.db.update_score(old_score, new_score)
        self.db.commit()
        self.pull_status()
        
    def RT_del(self, t_no) :
        self.db.add_log = []
        self.db.add_log.append('RT_DEL;{};{};'.format(t_no, self.variables['RT'][t_no][0]))
        self.db.delete_recurring_task(t_no)
        self.db.commit()
        self.pull_status()
        
    def RT_update(self, t_no, new_name, new_point) :
        self.db.add_log = []
        self.db.add_log.append('RT_UPDATE;{};{};{};{};'.format(t_no, self.variables['RT'][t_no][0], new_name, new_point))
        self.db.update_recurring_task(t_no, new_name, new_point)
        self.db.commit()
        self.pull_status()