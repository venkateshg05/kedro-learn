import pdb, sys, traceback, logging, yaml
from os.path import join

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro_datasets.pandas import CSVDataSet

class HooksHelperUtil:
    def __init__(self) -> None:
        with open('conf/local/credentials.yml', 'r') as credfile:
            credentials = yaml.safe_load(credfile)
        self.aws_key = credentials['dev_s3']['key']
        self.aws_secret = credentials['dev_s3']['secret']
    
    def generate_input_file_names(self, name):
        """
        returns a list of input items 
        to be added to catalog
        """
        inputs = [
            {
                'data_set_name': name,
                'data_set': CSVDataSet(
                    filepath = join(
                        's3://kedro-model-outputs/data/01_raw/', name + '.csv'
                    ),
                    credentials = dict(
                        key=self.aws_key,
                        secret=self.aws_secret
                    )
            ),
            }
        ]

        return inputs


class ProjectHooks:
    @property
    def _logger(self):
        return logging.getLogger(__name__)

    # debugging hooks
    @hook_impl
    def on_node_error(self):
        _, _, traceback_obj = sys.exc_info()
        traceback.print_tb(traceback_obj)
        pdb.post_mortem(traceback_obj)

    @hook_impl
    def on_pipeline_error(self):
        _, _, traceback_obj = sys.exc_info()
        traceback.print_tb(traceback_obj)
        pdb.post_mortem(traceback_obj)

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog) -> None:
        self.curr_catalog = catalog.list()
        self.catalog = catalog
        datasets = self.catalog.load('params:datasets')
        hooksHelperUtil = HooksHelperUtil()
        for name, dataset in datasets.items():
            generate_kws_list = hooksHelperUtil.generate_input_file_names(name)
            for kws in generate_kws_list:
                self.catalog.add(**kws)
        self._logger.info(
            f"""{'-'*10} 
            after_catalog_created
            Added the following to catalog
            {set(self.catalog.list()).difference(self.curr_catalog)}
            {'-'*10}"""
            )