import pdb, sys, traceback, logging
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog

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
        self._logger.info(catalog.list())