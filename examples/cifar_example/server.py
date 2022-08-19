from typing import Dict, Optional, Tuple
from pathlib import Path
import utils
import flwr as fl
import os
import tensorflow as tf
from fed_pack.trainer import ServerController


data_dir, server_ip, partition, filename = '', '', '', ''
def main() -> None:
    global data_dir
    global server_ip 
    global partition
    global filename
    global monitor_ip
    data_dir = os.environ['data_dir']
    server_ip = os.environ['server_ip']
    monitor_ip = os.environ['monitor_ip']
    print(server_ip)
    partition = os.environ['partition']
    filename = os.environ['filename']
    # Load and compile model for
    # 1. server-side parameter initialization
    # 2. server-side parameter evaluation
    model = tf.keras.applications.EfficientNetB0(
        input_shape=(32, 32, 3), weights=None, classes=10
    )
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    path = "/data/" + filename
    X, y = load_cifar(path, split=False)    
    scontrol = ServerController()
    scontrol.set_model(model)
    scontrol.set_data(X, y)
    scontrol.set_ips(server_ip, monitor_ip)
    scontrol.start(num_rounds=2, evaluate_func=evaluate_func)
    # Create strategy
    
def evaluate_func(model, X, y):
    loss, accuracy = model.evaluate(X, y)
    return loss, accuracy

def load_cifar(path, split=True):
    def unpickle(file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
    dataset = unpickle(path) #
    import numpy as np
    data = dataset[b'data']
    labels = np.array(dataset[b'labels']).reshape((-1, 1))
    data_reshaped = data.reshape((-1, 3, 32, 32))
    data_transposed = np.transpose(data_reshaped, axes=[0, 2, 3, 1])
    from sklearn.model_selection import train_test_split
    if split: 
        X_train, X_test, y_train, y_test = train_test_split(data_transposed, labels, random_state=0, test_size= 0.2)
        return X_train, X_test, y_train, y_test
    else: return data_transposed, labels

if __name__ == "__main__":
    main()