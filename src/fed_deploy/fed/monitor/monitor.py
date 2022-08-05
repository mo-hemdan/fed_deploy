from flask import Flask, redirect, url_for, request
import json

app = Flask(__name__)
metrics_log = {}

@app.route("/get_metrics", methods=["GET"])
def get_metrics():
    try:
        type = request.args.get('type')
        print("Type: ", type)
        ip_addr = request.args.get('ip_addr')
        print("Client IP: ", ip_addr)
        response = {
            "type": type, 
            "ip_addr": ip_addr,
            "params": None
        }
        if type in metrics_log.keys():
            if type == 'client':
                response["params"] = metrics_log[type][ip_addr]
            else:
                response["params"] = metrics_log[type]

        response = json.dumps(response)
        return response
    except Exception as e:
        return e

@app.route("/get_all_metrics", methods=["GET"])
def get_all_metrics():
    try:
        # host_ip_addr = "10.10.10.10"
        # response = {
        #     "type": "client", 
        #     "ip_addr": host_ip_addr,
        #     "round": 5,
        #     "epoch": 20,
        #     "params": {
        #         "accuracy": 0.68, 
        #         "loss": 689, 
        #         "val_accuracy": 0.55, 
        #         "val_loss": 750, 
        #     }
        # }
        # response = {
        #     "type": "client", 
        #     "ip_addr": host_ip_addr,
        #     "round": 5,
        #     "epoch": 20,
        #     "params": {
        #         "accuracy": 0.68, 
        #         "loss": 689, 
        #         "val_accuracy": 0.55, 
        #         "val_loss": 750, 
        #     }
        # }
        response = metrics_log
        response = json.dumps(response)
        return response
    except Exception as e:
        return e

@app.route("/post_metrics", methods=["POST"])
def post_metrics():
    try:
        content = request.get_json(force=True)

        type = content['type']
        ip_addr = content['ip_addr']
        round = content['round']
        accu = content['Params']['accuracy']
        loss = content['Params']['loss']
        val_accu = content['Params']['val_accuracy']
        val_loss = content['Params']['val_loss']

        if type not in metrics_log.keys():
            metrics_log[type] = {}
        if type == 'client':
            # Check if the required field is in the dictionary
            if ip_addr not in metrics_log[type].keys():
                metrics_log[type][ip_addr] = {}
            if round not in metrics_log[type][ip_addr].keys():
                metrics_log[type][ip_addr][round] = {}
            # Assign the required field to the specific value
            metrics_log[type][ip_addr][round]['accuracy'] = accu
            metrics_log[type][ip_addr][round]['loss'] = loss
            metrics_log[type][ip_addr][round]['val_accuracy'] = val_accu
            metrics_log[type][ip_addr][round]['val_loss'] = val_loss
        else:
            if round not in metrics_log[type].keys():
                metrics_log[type][round] = {}
            metrics_log[type][round]['accuracy'] = accu
            metrics_log[type][round]['loss'] = loss

        return "Okay"
    except Exception as e:
        return e

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)