import atexit
from fitsviz.utils.dask_utils import create_dask_client
from fitsviz.utils.dask_utils import cleanup_dask_client
# Create the Dask Client when the package is imported

client = create_dask_client()
print("Dask client initialized!")
atexit.register(cleanup_dask_client,client)