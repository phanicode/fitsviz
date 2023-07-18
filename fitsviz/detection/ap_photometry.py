
from fitsviz.utils import dask_utils as du
import dask
from astropy.io import fits
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from fitsviz.detection.core import DetectionBase
import pandas as pd
import numpy as np
from numba import jit
import concurrent.futures


class ApertureDAO(DetectionBase):
    """
    Args:
        DetectionBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        pass


    #@dask.delayed
    def process_sources(self, sources, sci_img_list):
        """
        Given a list of sources,get mean flux and spectral index

        Args:
            sources (pd.DataFrame):

        Returns:
            _type_: _description_
        """

        # Convert QTable to pandas and select centroids
        positions = sources["xcentroid", "ycentroid"].to_pandas()
        # print(positions)
        # Initialize pandas dataframe with source numbers as columns
        flux_df = pd.DataFrame(columns=positions.index)

        for sci in sci_img_list:

            sciimg = du.load_fits(sci)
            # print('science image',sciimg)
            median = np.nanmedian(du.sci_to_rms(sci))

            # print('rms image',rmsimg)
            
            # print('rms median',median)
            flux_accross_frequencies = []
            # median subtraction
            adj_sci = sciimg - median
            # print('adjusted science image',adj_sci)
            # go through every source and find its flux
            for _, row in positions.iterrows():

                x = int(row[0])
                y = int(row[1])
                # flux is crudely defined as sum of values inside aperture
                flux = np.nansum(adj_sci[y - 5: y + 5, x - 5: x + 5])

                flux_accross_frequencies.append(flux)

            # print('flux :',flux_accross_frequencies)
            flux_df.loc[len(flux_df)] = flux_accross_frequencies

        # get frequencies of all files
        freqs = [fits.getheader(sci)['CRVAL3'] for sci in sci_img_list]
        # transpose flux dataframe and iterate accross rows
        flux_df = flux_df.T
        # calculate spectral index of each source
        flux_df["spectral_index"] = [
            du.calculate_spectral_indices(freqs, row) for _, row in flux_df.iterrows()
        ]
        # rows: x coordinate, y coordinate,flux of lowest frequency,spectral
        # index of source
        lowest_idx = np.argmin(freqs)
        summary = positions.join(flux_df[[lowest_idx, "spectral_index"]])
        summary = summary.rename(columns={lowest_idx: "flux"})

        return summary
    
    def get_sources(self, science_data, rms_data):
        """Given science and rms files, apply the DAOStarFinder
        source detection algorithm to get summary statistics
        on those files.

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data

        Returns:
            sources,summary (np.ndarray,list): List of sources and summary statistics
        """

        mean, median, _ = sigma_clipped_stats(rms_data, sigma=3.0)

        daofind = DAOStarFinder(fwhm=3.0, threshold=5. * mean)

        sources = daofind(science_data - median)



        return sources

