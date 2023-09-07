"""
This is a boilerplate pipeline 'c_eval'
generated using Kedro 0.18.12
"""

import logging

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import calculate_model_performance
from kedro_learn.kedro_util import get_kedro_context

logger = logging.getLogger(__name__)


def create_pipeline_template() -> Pipeline:
    nodes = [
        node(
        calculate_model_performance,
        inputs=['model', 'test_x', 'test_y'],
        outputs='model_perf_metrics',
        name="calculate_model_performance"
        )
    ]

    return pipeline(nodes)

def create_pipeline(**kwargs) -> Pipeline:

    data_prep_pipeline_template = create_pipeline_template()

    context = get_kedro_context()
    datasets = context.params['datasets']
    
    data_prep_pipelines = []
    for name, dataset in datasets.items():
        data_prep_pipelines.append(
            pipeline(
                pipe = data_prep_pipeline_template,
                # inputs = inputs,
                namespace = name,
            )
        )

    logger.info(f"{'-'*10} \n{sum(data_prep_pipelines)}\n{'-'*10}")
    return sum(data_prep_pipelines)
