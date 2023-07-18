import atexit
from fitsviz.utils.dask_utils import create_dask_client
from fitsviz.utils.dask_utils import cleanup_dask_client
from fitsviz import detection
# Create the Dask Client when the package is imported
