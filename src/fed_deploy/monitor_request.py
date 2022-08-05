import requests
import json

# server_ip = "0.0.0.0"
# server_ip = "127.0.0.1"
monitor_ip = "188.185.11.183"
# monitor_ip = "188.185.120.31"
server_ip = monitor_ip

import socket
hostname=socket.gethostname()
host_ip_addr=socket.gethostbyname(hostname)

post = False
get = True

if post:
    post_content = json.dumps({
        "type": "server", 
        "ip_addr": None, 
        "round": 9,
        "epoch": 13,
        "Params": {
            "accuracy": 0.99, 
            "loss": 467, 
            "val_accuracy": 0.87, 
            "val_loss": 432, 
        }
    })
    result = requests.post("http://"+server_ip+":5050/post_metrics", data=post_content)
    print("Connection Status: ", result)
    print("Content Recieved: ", result.text)

    post_content = json.dumps({
        "type": "client", 
        "ip_addr": host_ip_addr,
        "round": 5,
        "epoch": 20,
        "Params": {
            "accuracy": 0.68, 
            "loss": 689, 
            "val_accuracy": 0.55, 
            "val_loss": 750, 
        }
    })
    result = requests.post("http://"+server_ip+":5050/post_metrics", data=post_content)
    print("Connection Status: ", result)
    print("Content Recieved: ", result.text)

if get:
    # GET SERVER Params
    get_params = {
        "type": "server", 
        "ip_addr": None, 
    }
    result = requests.get("http://"+server_ip+":5050/get_metrics", params=get_params)
    print("Connection Status: ", result)
    print("Content Recieved: ", result.json())

    # GET All Metrics
    result = requests.get("http://"+server_ip+":5050/get_all_metrics")
    print("Connection Status: ", result)
    print("Content Recieved: ", result.text)
    # print("Content Recieved: ", result.json())

    # GET Client Params
    # get_params = {
    #     "type": "client", 
    #     "ip_addr": "188.185.87.9", # host_ip_addr,
    # }
    # result = requests.get("http://"+server_ip+":5050/get_metrics", params=get_params)
    # print("Connection Status: ", result)
    # print("Content Recieved: ", result.json())
