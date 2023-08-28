"""
This is a boilerplate pipeline 'a_data_prep'
generated using Kedro 0.18.12
"""


import logging

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import clean, engineer_features
from kedro_learn.kedro_util import get_kedro_context

logger = logging.getLogger(__name__)

def create_pipeline(**kwargs) -> Pipeline:

    nodes = [
        node(
        clean,
        inputs=['params:datasets', 'params:clean'],
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

    data_prep_pipeline_template = pipeline(nodes)

    context = get_kedro_context()
    datasets = context.params['datasets']
    
    data_prep_pipelines = []
    for name, dataset in datasets.items():
        parameters = {
            'params:datasets': 'params:datasets.' + name,
            'params:clean': 'params:clean',
            'params:fe': 'params:fe'
        }
        data_prep_pipelines.append(
            pipeline(
                pipe = data_prep_pipeline_template,
                parameters = parameters,
                namespace = name,
            )
        )

    logger.info(sum(data_prep_pipelines))
    return sum(data_prep_pipelines)
