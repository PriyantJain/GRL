from . import extra_standard_tasks_routes
from . import daily_tasks_routes
from . import to_do_routes
from . import recurring_tasks_routes
from . import basic_details_routes
from . import vouchers_routes

import datetime
import flask

def add_routes(app, player) :
    extra_standard_tasks_routes.add_routes(app, player)
    daily_tasks_routes.add_routes(app, player)
    to_do_routes.add_routes(app, player)
    recurring_tasks_routes.add_routes(app, player)
    basic_details_routes.add_routes(app, player)
    vouchers_routes.add_routes(app, player)

    
    ## Home page rendering function
    def loaded_home_page() :
        to_do_done = player.get_to_do_done()
        to_do_done.sort(key = lambda x : x[5], reverse = True)
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")

        to_do, to_do_list = player.get_to_do_list()
        RT, RT_list = player.get_RT_list()

        lim = 0
        while lim < len(to_do_done) and to_do_done[lim][5] == _today : lim += 1
        lim = max(5, lim)

        variables = {'score' : player.score,
                     'membership' : player.membership,
                     'DT1' : player.dt1,
                     'DT2' : player.dt2,
                     'DT3' : player.dt3,
                     'DT1_done' : player.dt1_done,
                     'DT2_done' : player.dt2_done,
                     'DT3_done' : player.dt3_done,
                     'to_do' : to_do,
                     'to_do_list' : to_do_list,
                     'to_do_done' : to_do_done[:lim],
                     'today_target' : player.today_target,
                     'left_points' : max(player.today_target - player.score, 0),
                     'RT' : RT,
                     'RT_list' : RT_list,
                     'recurring_tasks_done' : player.get_RT_done()
                    }

        return flask.render_template("index.html", **variables)

    @app.route('/', methods = ['GET'])
    def home() : 
        player.pull_status()
        player.new_day()

        return loaded_home_page()
        
    
    def loaded_shop_page() :
        variables = {'Vouchers' : player.get_vouchers(),
                     'score' : player.score}
        return flask.render_template("Shop.html", **variables)
    
    @app.route('/shop', methods = ['GET'])
    def shop() :
        player.pull_status()

        return loaded_shop_page()