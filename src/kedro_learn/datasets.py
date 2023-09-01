import os, boto3, yaml, typing
import numpy as np

from pathlib import Path, PurePosixPath
from kedro.io import AbstractDataSet

from tensorflow.keras import Model
from tensorflow.keras.models import load_model

class S3ModelDataset(AbstractDataSet):
    def __init__(self, table):
        cred = "../conf/local/credentials.yml"
        with open(cred, 'r') as cred_file:
            creds = yaml.safe_load(cred_file)
        
        self.s3 = boto3.Session(
            aws_access_key_id=creds['dev_s3']['key'],
            aws_secret_access_key=creds['dev_s3']['secret'],
            region_name=creds['dev_s3']['default-region'],
        ).resource('s3')
        
    
    def _load(self) -> np.ndarray:
        return np.load(self._filepath)
    
    def _save(self, arr: np.ndarray) -> None:
        np.save(self._filepath, arr)
    
    def _exists(self):
        return Path(self._filepath.as_posix()).exists()

    def _describe(self):
        return dict( filepath = self._filepath, )