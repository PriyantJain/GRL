import flask
from flask import Flask
from GRL_class import GRL
player = GRL() 

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    
    if flask.request.method == 'POST' :
        if 'DT_B1' in flask.request.form : player.dt1_done = 1 - player.dt1_done
        if 'DT_B2' in flask.request.form : player.dt2_done = 1 - player.dt2_done
        if 'DT_B3' in flask.request.form : player.dt3_done = 1 - player.dt3_done
        return flask.redirect(flask.url_for('home'))

    variables = {'score' : player.score,
                 'membership' : player.membership,
                 'DT1' : player.dt1,
                 'DT2' : player.dt2,
                 'DT3' : player.dt3,
                 'DT1_done' : player.dt1_done,
                 'DT2_done' : player.dt2_done,
                 'DT3_done' : player.dt3_done,
                 'to_do' : player.get_to_do_list(),
                 'recurring_tasks' : player.get_recurring_tasks()
                }
    
    return flask.render_template("index.html", **variables)


if __name__ == '__main__' : 
    app.run()
