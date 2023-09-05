import os, boto3, logging
import numpy as np

from pathlib import Path, PurePosixPath
from kedro.io import AbstractDataSet

from tensorflow.keras.models import load_model

class S3ModelDataset(AbstractDataSet):
    @property
    def _logger(self):
        return logging.getLogger(__name__)
    
    def __init__(self, filepath, credentials, fs_args):
        self.fs_args = fs_args
        self.s3_filepath = f"{'/'.join(filepath.split('/')[3:])}.{self.fs_args['save_format']}"
        self.local_filepath = os.path.join(
            'data', '06_models', f"{filepath.split('/')[-1]}.{self.fs_args['save_format']}"
            )
        self.s3 = boto3.Session(
            aws_access_key_id=credentials['key'],
            aws_secret_access_key=credentials['secret'],
            region_name=credentials['default-region'],
        ).client('s3')
        
    
    def _load(self) -> np.ndarray:
        return load_model(self.local_filepath)
    
    def _save(self, model) -> None:
        model.save(
            PurePosixPath(self.local_filepath), 
            # save_format=self.fs_args['save_format']
            )
        response = self.s3.upload_file(
            self.local_filepath,
            self.fs_args['s3_bucket'],
            self.s3_filepath
            )
        self._logger.info(str(response))
    
    def _exists(self):
        return Path(self._filepath.as_posix()).exists()

    def _describe(self):
        return dict( filepath = self.local_filepath, )