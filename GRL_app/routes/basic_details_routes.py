import flask

def add_routes(app, player):
    @app.route('/score', methods = ['GET'])
    def score() :   return flask.jsonify(player.score)

    @app.route('/membership', methods = ['GET'])
    def membership() :  return flask.jsonify(player.membership)

    @app.route('/left_points', methods = ['GET'])
    def left_points() :  return flask.jsonify(max(player.today_target - player.score, 0))
    