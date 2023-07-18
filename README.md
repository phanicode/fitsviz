# fitsviz

fitsviz is a Python package that provides functionality for visualizing and analyzing FITS (Flexible Image Transport System) files. It includes two main commands: `mkstat` and `mkviz`. 

## Installation

To install fitsviz, you can use pip and the provided `pyproject.toml` file:

`pip install fitsviz`


## Usage

### mkstat Command
```
The `mkstat` command is used to identify objects from the science image at the lowest frequency. It supports the following options:

Usage: fitsviz mkstat [OPTIONS]

Identify objects from the science image at the lowest frequency

Options:
-i, --input_dir PATH Path to the directory containing the science images
-od, --output_dir PATH Output directory for the detected CSV file
-o, --output_file_name TEXT Detected CSV file name
-a, --algorithm [aperture|naive]
Source detection algorithm
```


Copy code

Example usage:

fitsviz mkstat -i path/to/science_images -od path/to/output_dir -o detected.csv -a aperture




### mkviz Command
```

The `mkviz` command is used to visualize the lowest frequency science image in a directory. It supports the following options:

Usage: fitsviz mkviz [OPTIONS]

Visualize the lowest frequency science image in a directory

Options:
`-i, --input_dir PATH Path to the directory containing the science images
-b, --backend [matplotlib|bokeh]
Visualization backend
```




Example usage:

fitsviz mkviz -i path/to/science_images -b matplotlib



## Dependencies

The fitsviz package depends on the following libraries and versions:

- astropy==5.3.1
- bokeh==3.2.0
- click==8.0.4
- dask==2021.10.0
- matplotlib==3.4.3
- numba==0.54.1
- numpy==1.22.3
- pandas==2.0.3
- photutils==1.8.0
- setuptools==58.0.4

Please ensure that these dependencies are installed in your Python environment.

## Build Information

The package uses the "setuptools" build backend, as specified in the `pyproject.toml` file.
