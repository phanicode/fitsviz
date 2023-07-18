import matplotlib.pyplot as plt
import numpy as np
import dask as da
from fitsviz.utils import dask_utils as du
from astropy.stats import sigma_clipped_stats
from photutils import DAOStarFinder
from photutils import CircularAperture
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from fitsviz.detection.ap_photometry import ApertureDAO


def da_visualize(sci_img, rms_img):
    # Load science img
    # da.from_array(fits.getdata(file)[0,0,:,:])
    sci_data = du.load_fits(sci_img)
    # Load rms by parsing file
    rms_median = np.nanmedian(du.load_fits(rms_img))

    # get the list of sources and summary_stats
    sources = ApertureDAO.get_sources(sci_data, rms_data)

    # list of positions to visualize
    positions = da.transpose((sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(positions, r=100.0)

    norm = ImageNormalize(stretch=SqrtStretch())

    plt.imshow(sci_data - summary_stats[0],
               cmap='viridis',
               origin='lower',
               norm=norm,
               interpolation='nearest')
    plt.colorbar()
    apertures.plot(color='blue', lw=1.5, alpha=0.5)
    plt.show()
