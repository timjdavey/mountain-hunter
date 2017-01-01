from utils import find_peaks, verify_prominence
import numpy as np

DIMENSION_3 = 1201
DIMENSION_1 = 3601
MOUNTAIN_HEIGHT = 2500
SUBPEAK_PROMINENCE = 30
PEAK_RESOLUTION = 300


class MountainFinder:
    """
    Helper object for finding mountains within a given SRTM dataset

    NASA Shuttle Radar Topography Mission
    http://vterrain.org/Elevation/SRTM/

    Format information
    www2.jpl.nasa.gov/srtm/faq.html

    Data source
    http://www.viewfinderpanoramas.org/dem3.html#nasa

    About the data, given file e.g. n51e002.hgt
    * represents the area 51N 2E (south west corner) to 52N 3E
    * similarly s14w077.hgt covers 14S 77W to 13S 76W
    * TODO? Is the projection of data reversed for SW values?
    * .hgt simply means "height"
    * elevation measured in meters above sea level
    * data voids indicated by -32768
    * Big-endian 2 byte format

    Definition of a mountain
    https://en.wikipedia.org/wiki/Mountain

    Definition of a peak
    https://en.wikipedia.org/wiki/Topographic_prominence

    """

    def __init__(self, filename,
                 north=None, east=None, south=None, west=None,
                 dimension=DIMENSION_3,
                 size_check=False, clean=0):
        # convert north east to lat long standards
        # for south and west values, subtract 1 to represent consistent corner
        if not (isinstance(north, int) or isinstance(south, int)):
            raise ValueError("Please provide north or south as int")
            if south:
                north = -south - 1
        if not (isinstance(east, int) or isinstance(west, int)):
            raise ValueError("Please provide east or west as int")
            if west:
                east = -west - 1

        # check file dimensions
        if size_check:
            dim = self.check_data(filename)
        else:
            dim = dimension

        # >i2 is big-endian short signed int format
        self.raw = np.fromfile(filename, np.dtype(
            '>i2'), dim * dim)

        # clean raw data
        self.clean(clean)

        # other data items
        self.latitude = north  # y
        self.longitude = east  # x
        self.dimension = dim

        # initialise for plotting
        self.surface = np.copy(self.raw).reshape(
            (self.dimension, self.dimension))

    def check_data(self, filename):
        """
        Given a local file path str
        Each cell has 2 bytes, the elevation is 256*()
        Great answer below on data reading
        http://stackoverflow.com/questions/357415/how-to-read-nasa-hgt-binary-files
        Returns the dimension
        """
        import math
        import os
        siz = os.path.getsize(filename)
        dim = int(math.sqrt(siz / 2))
        assert dim * dim * 2 == siz, 'Invalid file size'
        return dim

    def clean(self, min_height):
        """
        Permanently alters the data on this object.
        Used to 'level' any data voids with sea level.
        * required min_height, removes all data below this height
        * optional set_to_height (default 0), sets the data to this value
        """
        np.place(self.raw, self.raw < min_height, 0)

    def find_peaks(self, resolution, min_height, prominence, distance):
        """
        Finds all the peaks, ranked by heightest. See utils.find_peaks for details
        """
        all_peaks = find_peaks(self.surface, resolution, min_height)
        verified = verify_prominence(
            self.surface, all_peaks, prominence, distance, 360)
        self.raw_peaks = [p[0] for p in verified]
        self.peaks_with_contours = verified
        return verified

    def peaks(self):
        """
        Returns list of peaks with global position
        as (height, latitude, longitude) in decimal ord format
        """
        try:
            self.raw_peaks
        except:
            raise NameError("Please run find_peaks before asking for peaks()")
        else:
            latlng_peaks = []
            for p in self.raw_peaks:
                p = (p[0],
                     self.latitude + (p[1] / (self.dimension - 1)),
                     self.longitude + (p[1] / (self.dimension - 1))
                     )
                latlng_peaks.append(p)
            self.latlng_peaks = latlng_peaks
            return self.latlng_peaks

    def plot(self, contours=True):
        """
        Plots the peaks and the projected land
        If find_peaks has not been run, will only plot the land
        """
        import matplotlib.pyplot as pp
        # plot leveled data
        pp.imshow(self.surface, cmap='spectral')
        pp.colorbar()
        # plot peaks
        try:
            self.raw_peaks
        except:
            # TODO: log warning that no peaks found
            pass
        else:
            markers = ['.', 'o', 'p', '8', '*',
                       'x', 'D', 'd', '1', '2', '3', '4']
            len_m = len(markers)
            if contours:
                for i, p in enumerate(self.peaks_with_contours):
                    x, y = [], []
                    x.append(p[0][2])
                    y.append(p[0][1])
                    for c in p[1]:
                        x.append(c[2])
                        y.append(c[1])
                    pp.scatter(x, y, color='blue', marker=markers[i%len_m])
            else:
                x, y = [], []
                for p in self.raw_peaks:
                    x.append(p[2])
                    y.append(p[1])
                pp.scatter(np.array(x), np.array(y), color='blue', marker='x')
            #a, b = [], []
            # for p, contours in self.contours:
            #    for c in contours:
            #        a.append(c[2])
            #        b.append(c[1])
            #pp.scatter(np.array(a), np.array(b), color='black', marker='+')
        pp.show()


if __name__ == '__main__':
    north = '44'
    east = '078'
    filename = 'L%s/N%sE%s.hgt' % (north, north, east)
    info = MountainFinder(filename, north=int(north), east=int(east), clean=0)
    peaks = info.find_peaks(3, 2500, 150, 200)
    info.plot()
