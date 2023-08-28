import os, logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def clean(dataset:dict, clean_params:dict) -> pd.DataFrame:
    logger.info(f"dataset: {dataset}")
    logger.info(f"clean params: {clean_params}")
    clean_df = pd.DataFrame(data=[[1,2], [1,2]], columns=['a', 'b'])
    return [clean_df]

def engineer_features(clean_df:pd.DataFrame, fe_params:dict)-> pd.DataFrame:
    logger.info(f"clean_df.columns {clean_df}")
    logger.info(f"fe_params {fe_params}")
    clean_df['c'] = clean_df['a'] + clean_df['b']
    return [clean_df]
