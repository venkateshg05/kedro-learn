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
    
class DDBModelMetrics(AbstractDataSet):
    @property
    def _logger(self):
        return logging.getLogger(__name__)
    
    def __init__(self, tablename, credentials):
        self.ddb_table = boto3.Session(
            aws_access_key_id=credentials['key'],
            aws_secret_access_key=credentials['secret'],
            region_name=credentials['default-region'],
        ).resource('dynamodb')\
        .Table(tablename)
        
    
    def _load(self) -> np.ndarray:
        return self.ddb_table.table_name
    
    def _save(self, item) -> None:
        response = self.ddb_table.put_item(
            Item=item
        )
        self._logger.info(
            f"HTTPStatusCode: {str(response['HTTPStatusCode'])}\n"
            f"Date: {str(response['HTTPHeaders']['Date'])}\n"
            )
    
    def _exists(self):
        return self.ddb_table.table_status == 'ACTIVE'

    def _describe(self):
        return dict(
            tablename = self.ddb_table.table_name,
            status = self.ddb_table.table_status,
            schema = self.ddb_table.key_schema
        )