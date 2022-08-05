import argparse
import os
from pathlib import Path

import tensorflow as tf
import utils
import flwr as fl

# Make TensorFlow logs less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
monitor_ip = "188.185.11.183"
# monitor_ip = "188.185.120.31"
server_ip = "188.185.11.183"
client_id = "DefaultHOSTNAME"

# Define Flower client
class CifarClient(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test

    def get_properties(self, config):
        """Get properties of client."""
        raise Exception("Not implemented")

    def get_parameters(self):
        """Get parameters of the local model."""
        raise Exception("Not implemented (server-side parameter initialization)")

    def fit(self, parameters, config):
        """Train parameters on the locally held training set."""
        global client_id

        # Update local model parameters
        self.model.set_weights(parameters)

        # Get hyperparameters for this round
        batch_size: int = config["batch_size"]
        epochs: int = config["local_epochs"]
        server_round: int = config["server_round"]

        # Train the model using hyperparameters from config
        history = self.model.fit(
            self.x_train,
            self.y_train,
            batch_size,
            epochs,
            validation_split=0.1,
        )

        # Return updated model parameters and results
        parameters_prime = self.model.get_weights()
        num_examples_train = len(self.x_train)


        results = {
            "loss": history.history["loss"][0],
            "accuracy": history.history["accuracy"][0],
            "val_loss": history.history["val_loss"][0],
            "val_accuracy": history.history["val_accuracy"][0],
        }
        his_summary = history.history

        result = utils.post_metrics(
            monitor_ip = monitor_ip,
            type = "client",
            ip_addr = client_id, 
            round = server_round,
            accuracy = his_summary["accuracy"], 
            loss = his_summary["loss"],
            val_accuracy = his_summary["val_accuracy"], 
            val_loss = his_summary["val_loss"],
        )
        print("Content Recieved: ", result.text)

        return parameters_prime, num_examples_train, results

    def evaluate(self, parameters, config):
        """Evaluate parameters on the locally held test set."""

        # Update local model with global parameters
        self.model.set_weights(parameters)

        # Get config values
        steps: int = config["val_steps"]

        # Evaluate global model parameters on the local test data and return results
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test, 32, steps=steps)
        num_examples_test = len(self.x_test)
        return loss, num_examples_test, {"accuracy": accuracy}


def main() -> None:
    # Parse command line argument `partition`
    global client_id
    print(os.environ['client_ip'])
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument("--partition", type=str, required=True) #choices=range(0, 10), )
    parser.add_argument("--client_id", type=str, required=True) #choices=range(0, 10), )
    parser.add_argument("--filename", type=str, required=True) #choices=range(0, 10), )
    args = parser.parse_args()
    client_id = args.client_id
    print("Client ID: ", client_id)
    print("Partition: ", int(args.partition))

    # Load and compile Keras model
    model = tf.keras.applications.EfficientNetB0(
        input_shape=(32, 32, 3), weights=None, classes=10
    )
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    # Load a subset of CIFAR-10 to simulate the local data partition
    # path = "/data/data_batch_3"
    path = "/data/" + args.filename
    x_train, x_test, y_train, y_test = load_cifar(path)
    # (x_train, y_train), (x_test, y_test) = load_partition(int(args.partition))

    # Start Flower client
    client = CifarClient(model, x_train, y_train, x_test, y_test)

    fl.client.start_numpy_client(
        server_address=server_ip+":8080",
        client=client,
        #root_certificates=Path(".cache/certificates/ca.crt").read_bytes(),
    )


def load_partition(idx: int):
    """Load 1/10th of the training and test data to simulate a partition."""
    assert idx in range(10)
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    return (
        x_train[idx * 5000 : (idx + 1) * 5000],
        y_train[idx * 5000 : (idx + 1) * 5000],
    ), (
        x_test[idx * 1000 : (idx + 1) * 1000],
        y_test[idx * 1000 : (idx + 1) * 1000],
    )

def load_cifar(path):
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
    X_train, X_test, y_train, y_test = train_test_split(data_transposed, labels, random_state=0, test_size= 0.2)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    main()