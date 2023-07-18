from abc import ABC, abstractmethod, ABCMeta
import numpy as np
from photutils import DAOStarFinder
from astropy.stats import sigma_clipped_stats
import dask


class DetectionBase(metaclass=ABCMeta):
    """Base class for detection algorithms,
    new algorithms should inherit from this class and implement
    the get_sources method.

    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.
    """
    @abstractmethod
    def get_sources(self, science_data, rms_data):
        """Given science and rms files, apply a custom detection algorithm

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data
        """
        pass
