import os, logging, time
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def clean(
        input_df:pd.DataFrame, 
        clean_params:dict
        ) -> pd.DataFrame:
    clean_df = input_df.round(2)
    logger.info(f"input.shape: {input_df.shape} \nclean_params: {clean_params}")
    return [clean_df]

def engineer_features(
        clean_df:pd.DataFrame, 
        fe_params:dict
        ) -> pd.DataFrame:
    logger.info(f"fe_params: {fe_params}")
    clean_df['C'] = clean_df['A'] + clean_df['B']
    return [clean_df]
