from . import extra_standard_tasks_routes
from . import daily_tasks_routes
from . import to_do_routes
from . import recurring_tasks_routes

import datetime
import flask

def add_routes(app, player) :
    extra_standard_tasks_routes.add_routes(app, player)
    daily_tasks_routes.add_routes(app, player)
    to_do_routes.add_routes(app, player)
    recurring_tasks_routes.add_routes(app, player)
    
    ## Basic page rendering get API calls
    def loaded_home_page() :
        to_do_done = player.get_to_do_done()
        to_do_done.sort(key = lambda x : x[2], reverse = True)
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")

        lim = 0
        while lim < len(to_do_done) and to_do_done[lim][2] == _today : lim += 1
        lim = max(5, lim)

        variables = {'score' : player.score,
                     'membership' : player.membership,
                     'DT1' : player.dt1,
                     'DT2' : player.dt2,
                     'DT3' : player.dt3,
                     'DT1_done' : player.dt1_done,
                     'DT2_done' : player.dt2_done,
                     'DT3_done' : player.dt3_done,
                     'to_do' : player.get_to_do_list(),
                     'to_do_done' : to_do_done[:lim],
                     'today_target' : player.today_target,
                     'recurring_tasks' : player.get_RT_list(),
                     'recurring_tasks_done' : player.get_RT_done(),
                     'TD_edit_state' : False
                    }

        return flask.render_template("index.html", **variables)

    @app.route('/GRL', methods=['GET'])
    def GRL_get():
        return loaded_home_page()

    @app.route('/', methods = ['GET'])
    def home() : 
        player.pull_status()
        player.new_day()

        return loaded_home_page()
        
    
