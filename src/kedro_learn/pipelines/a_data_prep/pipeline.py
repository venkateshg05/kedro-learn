"""
This is a boilerplate pipeline 'a_data_prep'
generated using Kedro 0.18.12
"""


import logging

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import clean, engineer_features
from kedro_learn.kedro_util import get_kedro_context

logger = logging.getLogger(__name__)


def create_pipeline_template() -> Pipeline:
    nodes = [
        node(
        clean,
        inputs=['input_df', 'params:clean'],
        outputs=['clean_data'],
        name="clean_input"
        ),
        node(
        engineer_features,
        inputs=['clean_data', 'params:fe'],
        outputs=['model_df'],
        name="feature_engg"
        )
    ]

    return pipeline(nodes)

def create_pipeline(**kwargs) -> Pipeline:

    data_prep_pipeline_template = create_pipeline_template()

    context = get_kedro_context()
    datasets = context.params['datasets']
    
    data_prep_pipelines = []
    for name, dataset in datasets.items():
        parameters = {
            'params:clean': 'params:clean',
            'params:fe': 'params:fe'
        }
        inputs = {
            'input_df' : name
        }
        data_prep_pipelines.append(
            pipeline(
                pipe = data_prep_pipeline_template,
                parameters = parameters,
                inputs = inputs,
                namespace = name,
            )
        )

    logger.info(f"{'-'*10} \n{sum(data_prep_pipelines)}\n{'-'*10}")
    return sum(data_prep_pipelines)
