from astropy.io import fits
import dask.array as da
import dask
from dask.distributed import Client
import numpy as np
import glob




def load_fits(file):
    return fits.getdata(file)[0, 0, :, :]


def sci_to_rms(file):
    """_summary_

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    file = file.replace("tt0.subim.fits", "tt0.rms.subim.fits")
    return fits.getdata(file)[0, 0, :, :]

def get_image_with_least_freq(science_images):
    cur_freq = 9223372036854775807
    least_freq_img = None

    for sci_img in science_images:
        sci_img_freq = fits.getheader(sci_img)['CRVAL3']
        if cur_freq > sci_img_freq:
            cur_freq = sci_img_freq
            least_freq_img = sci_img
    return least_freq_img


def create_dask_client(n_workers=4):
    client = Client(n_workers=n_workers)
    return client

def calculate_spectral_indices(frequencies, flux_densities):
    """
    Calculate the spectral index of a source given a list of frequencies and flux densities
    Args:
        frequencies (list[float]): List of frequencies
        flux_densities (list[float]): List of flux densities
        Returns:
            spectral_index (float): Spectral index of the source
    """
    log_frequencies = np.log10(frequencies)
    log_flux_densities = np.log10(flux_densities)

    # Fit a linear regression to calculate the spectral index
    coefficients = np.polyfit(log_frequencies, log_flux_densities, deg=1)
    spectral_index = coefficients[0]

    return spectral_index




def cleanup_dask_client(dask_client):
    if dask_client is not None:
        dask_client.close()
