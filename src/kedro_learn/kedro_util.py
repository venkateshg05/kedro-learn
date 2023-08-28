from pathlib import Path
from kedro.framework.session import KedroSession

def get_kedro_context(wd = None):
    if wd == None:
        wd = Path.cwd()
    session = KedroSession.create(
        package_name = 'kedro_learn', 
        project_path = wd
    )
    return session.load_context()