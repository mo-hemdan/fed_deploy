from typing import Dict, Optional, Tuple
from pathlib import Path
import utils
import flwr as fl
import tensorflow as tf


monitor_ip = "188.185.11.183"
# monitor_ip = "188.185.120.31"
def main() -> None:
    # Load and compile model for
    # 1. server-side parameter initialization
    # 2. server-side parameter evaluation
    model = tf.keras.applications.EfficientNetB0(
        input_shape=(32, 32, 3), weights=None, classes=10
    )
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    # Create strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.3,
        fraction_evaluate=0.2,
        min_fit_clients=3,
        min_evaluate_clients=2,
        min_available_clients=3,
        evaluate_fn=get_evaluate_fn(model),
        on_fit_config_fn=fit_config,
        on_evaluate_config_fn=evaluate_config,
        initial_parameters=fl.common.ndarrays_to_parameters(model.get_weights()),
    )

    # Start Flower server (SSL-enabled) for four rounds of federated learning
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=2),
        strategy=strategy,
        # certificates=(
        #     Path(".cache/certificates/ca.crt").read_bytes(),
        #     Path(".cache/certificates/server.pem").read_bytes(),
        #     Path(".cache/certificates/server.key").read_bytes(),
        # ),
    )


def get_evaluate_fn(model):
    """Return an evaluation function for server-side evaluation."""

    # Load data and model here to avoid the overhead of doing it in `evaluate` itself
    # (x_train, y_train), _ = tf.keras.datasets.cifar10.load_data()

    # # Use the last 5k training examples as a validation set
    # x_val, y_val = x_train[45000:50000], y_train[45000:50000]
    # x_tr, y_tr = x_train[:45000], y_train[:45000]
    
    path = "/data/data_batch_3"
    x_tr, x_val, y_tr, y_val = load_cifar(path)

    # The `evaluate` function will be called after every round
    def evaluate(
        server_round: int,
        parameters: fl.common.NDArrays,
        config: Dict[str, fl.common.Scalar],
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        model.set_weights(parameters)  # Update model with the latest parameters
        loss, accuracy = model.evaluate(x_tr, y_tr)
        val_loss, val_accuracy = model.evaluate(x_val, y_val)  

        result = utils.post_metrics(
            monitor_ip = monitor_ip,
            type = "server",
            ip_addr = None, 
            round = server_round,
            accuracy = accuracy, 
            loss = loss,
            val_accuracy = val_accuracy, 
            val_loss = val_loss,
        )
        print("Content Recieved: ", result.text)

        return val_loss, {"accuracy": val_accuracy}

    return evaluate


def fit_config(server_round: int):
    """Return training configuration dict for each round.
    Keep batch size fixed at 32, perform two rounds of training with one
    local epoch, increase to two local epochs afterwards.
    """
    config = {
        "batch_size": 32,
        "local_epochs": 1 if server_round < 2 else 2,
        "server_round": server_round,
    }
    return config


def evaluate_config(server_round: int):
    """Return evaluation configuration dict for each round.
    Perform five local evaluation steps on each client (i.e., use five
    batches) during rounds one to three, then increase to ten local
    evaluation steps.
    """
    val_steps = 5 if server_round < 4 else 10
    return {"val_steps": val_steps}
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