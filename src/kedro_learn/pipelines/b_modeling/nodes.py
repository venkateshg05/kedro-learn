"""
This is a boilerplate pipeline 'b_modeling'
generated using Kedro 0.18.12
"""
import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Activation, Dense, Dropout
from tensorflow.keras.models import Sequential

logger = logging.getLogger(__name__)

def split_data(model_df, model_input_config):
    X_train, X_test, y_train, y_test = train_test_split(
        model_df.iloc[:, 0:1],
        model_df.iloc[:, -1],
        test_size=model_input_config['train_test_split']
    )
    return X_train, X_test, y_train, y_test

def build_model(
        x_train, 
        y_train,
        nn_config,
        model_run_config
        ) -> pd.DataFrame:
    NN_model = Sequential()

    # The Input Layer :
    NN_model.add(Dense(
            128, 
            kernel_initializer=nn_config['kernel_initializer'],
            input_dim = x_train.shape[1], 
            activation=nn_config['activation']
        ))
    # The Hidden Layers :
    for _ in range(nn_config['num_hidden_layers']):
        NN_model.add(Dense(
                256, 
                kernel_initializer=nn_config['kernel_initializer'],
                activation=nn_config['activation']
            ))
    # The Output Layer :
    NN_model.add(Dense(
            1, 
            kernel_initializer=nn_config['kernel_initializer'],
            activation=nn_config['activation_final']
        ))

    # Compile the network :
    NN_model.compile(
        loss='mean_absolute_error', 
        optimizer='adam', 
        metrics=['mean_absolute_error']
        )
    logger.info(NN_model.summary())

    NN_model.fit(
        x_train, y_train, 
        batch_size=model_run_config['batch_size'], 
        epochs=model_run_config['epochs'], 
        verbose=model_run_config['verbose'], 
        validation_split=model_run_config['validation_split']
    )

    return [NN_model]
