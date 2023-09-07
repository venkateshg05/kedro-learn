"""
This is a boilerplate pipeline 'c_eval'
generated using Kedro 0.18.12
"""

import logging
import uuid
from datetime import datetime

from tensorflow.keras.metrics import kl_divergence, mae

logger = logging.getLogger(__name__)

def calculate_model_performance(model, test_x, test_y):
    perf_metrics = model.evaluate(x=test_x, y=test_y, return_dict=True)
    # pred_y = model.predict(test_x)
    # perf_metrics['mae'] = mae(test_y, pred_y)
    # perf_metrics['kl_divergence'] = kl_divergence(test_y, pred_y)
    perf_metrics = {
        k:str(round(v, 4)) for k,v in perf_metrics.items()
    }
    logger.info(
        perf_metrics
    )
    perf_metrics['model_id'] = str(uuid.uuid1())
    perf_metrics['model_run_dt'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    return perf_metrics