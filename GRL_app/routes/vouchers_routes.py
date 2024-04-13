import flask

def add_routes(app, player):
    # @app.route('/RT', methods=['GET'])
    # def get_recurring_tasks():    return flask.jsonify(player.get_RT_list())

    # @app.route('/RT/completed', methods=['GET'])
    # def get_RT_completed():    return flask.jsonify(player.get_RT_done())

    @app.route('/vouchers/create', methods = ['POST'])
    def createVoucher() :
        vName = flask.request.json.get('vName')
        vPrice = flask.request.json.get('vPrice')
        
        player.createVoucher(vName, vPrice)
        
        response = {'status': 'success'}
        return flask.jsonify(response), 201
    
    @app.route('/voucher/<int:vNo>/details', methods=['PUT'])
    def editVoucherDetails(vNo) :
        voucherName = flask.request.json.get('voucherName')
        voucherPrice = flask.request.json.get('voucherPrice')
        player.editVoucherDetails(vNo, voucherName, voucherPrice)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/voucher/<int:vNo>/buy/<int:q>', methods=['PUT'])
    def buyVoucher(vNo, q) :
        player.buyVoucher(vNo, q)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/voucher/<int:vNo>/use/<int:q>', methods=['PUT'])
    def useVoucher(vNo, q) :
        player.useVoucher(vNo, q)
        response = {'status': 'success'}
        return flask.jsonify(response)
