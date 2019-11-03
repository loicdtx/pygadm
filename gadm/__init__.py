import os
import tempfile
from pprint import pprint

import requests
import fiona

__version__ = "0.0.1"


class NoResultFound(Exception):
    pass


class NonUniqueCondition(Exception):
    pass


def url_retrieve(url, filename, overwrite=False, check_complete=False):
    """Generic file download function

    Similar to url_retrieve from standard library with additional checks for
    already existing files and incomplete downloads

    Args:
        url (str): Url pointing to file to retrieve
        filename (str): Local file name under which the downloaded content is
            written
        overwrite (bool): Force overwriting local file even when it already exists?
            Defaults to False
        check_complete (bool): When local file exists and overwrite is set to False,
            check whether local and remote file sizes match? File is re-downloaded
            when sizes are different. Only makes sense if overwrite is set to False.
            Defaults to True

    Returns:
        str: The filename
    """
    # Handle special cases (file already exists, no overwrite, check integrity)
    if os.path.isfile(filename) and not overwrite:
        if not check_complete:
            return filename
        r0 = requests.head(url)
        if os.path.getsize(filename) == int(r0.headers['Content-Length']): # file size matches 
            return filename
    # Proceed to download
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename


def get_data(code, level=0, force_download=False):
    # Build zip filename
    basename = 'gadm36_%s_gpkg.zip' % code.upper()
    filename = os.path.join(tempfile.gettempdir(), basename)
    gpkg = 'gadm36_%s.gpkg' % code.upper()
    layer = 'gadm36_%s_%d' % (code.upper(), level)
    url = 'https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/%s' % basename
    vfs = 'zip://%s' % filename
    # Run url_retrieve
    url_retrieve(url=url, filename=filename, overwrite=force_download)
    # Read as feature collection
    with fiona.open(gpkg, vfs=vfs, layer=layer) as con:
        fc = list(con)
    return FeatureCollection(fc)


class FeatureCollection(list):
    def get(self, **kwargs):
        if len(kwargs) > 1 or len(kwargs) == 0:
            raise ValueError('You must query a single key time')
        key, value = [*kwargs.items()][0]
        sub_fc = [feature for feature in self if feature['properties'][key] == value]
        if len(sub_fc) == 0:
            raise NoResultFound('No feature returned by query')
        elif len(sub_fc) > 1:
            raise NonUniqueCondition('Query matches multiple features')
        return sub_fc[0]

    def filter_by(self, **kwargs):
        if len(kwargs) > 1 or len(kwargs) == 0:
            raise ValueError('You can only filter on one key at the time')
        key, value = [*kwargs.items()][0]
        filtered_list = [feature for feature in self if feature['properties'][key] == value]
        return FeatureCollection(filtered_list)
