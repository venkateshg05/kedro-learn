"""
This is a boilerplate pipeline 'b_modeling'
generated using Kedro 0.18.12
"""

import logging

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import split_data, build_model
from kedro_learn.kedro_util import get_kedro_context

logger = logging.getLogger(__name__)


def create_pipeline_template() -> Pipeline:
    nodes = [
        node(
        split_data,
        inputs=['model_df', 'params:model_input_config'],
        outputs=['train_x', 'test_x', 'train_y', 'test_y'],
        name="split_data"
        ),
        node(
        build_model,
        inputs=['train_x', 'train_y', 'params:nn_config', 'params:model_run_config'],
        outputs=['model'],
        name="create_model"
        )
    ]

    return pipeline(nodes)

def create_pipeline(**kwargs) -> Pipeline:

    data_prep_pipeline_template = create_pipeline_template()

    context = get_kedro_context()
    datasets = context.params['datasets']
    
    data_prep_pipelines = []
    for name, dataset in datasets.items():
        inputs = {
            'input_df' : name
        }
        data_prep_pipelines.append(
            pipeline(
                pipe = data_prep_pipeline_template,
                inputs = inputs,
                namespace = name,
            )
        )

    logger.info(f"{'-'*10} \n{sum(data_prep_pipelines)}\n{'-'*10}")
    return sum(data_prep_pipelines)
