import numpy as np

# setup for iteration


class BreakOut(Exception):
    "Simple custom exception to break out of nested loops"
    pass

SURFACE_EMSG = "%s dimension too small. Neds to be at >= 2 larger than the locale %s"


def common_surface_checks(surface, locale):
    """
    Checks for common input errors
    Returns the dimension of the surface
    """
    # handle errors
    try:
        dimension = len(surface)
        dimension2 = len(surface[0])
    except IndexError:
        raise ValueError("Surface cannot be null")
    else:
        if dimension < locale + 2:
            raise ValueError(SURFACE_EMSG % (dimension, locale))
        if dimension != dimension2:
            raise ValueError("Surface must be a square")
    return dimension


def find_peaks(surface, locale=1, high_pass_filter=None):
    """
    Simple utility for finding the highest peak in a 2D surface
    Requires NxN dimension surface
    Returns a list of points
    Won't return peaks around edges

    TODO: expand to N dimensions
    """
    dimension = common_surface_checks(surface, locale)

    peaks = []
    # iterate over entire surface, skipping edges
    for i in range(locale, dimension - locale):
        for j in range(locale, dimension - locale):
            evaluated = surface[i][j]
            # must be larger than min_height (simple first check)
            if high_pass_filter is None or evaluated > high_pass_filter:
                try:
                    # find if largest within it's locale box
                    for y in range(-locale, locale + 1):
                        for x in range(-locale, locale + 1):
                            # don't check central pixel
                            if (y == 0 and x == 0):
                                pass
                            # if it's lower than reference, know it's not
                            elif evaluated <= surface[i + y][j + x]:
                                raise BreakOut("Is not highest in locale")
                except BreakOut:
                    # if not the highest, then ignore and continue
                    pass
                else:
                    # otherwise it is! and add to list
                    # need to add back locale to position
                    # to account for skipped edges
                    peaks.append((evaluated, i, j))
    return peaks


def verify_prominence(surface, peaks, prominence, distance_threshold, angles=8):
    """
    Key assumption is if can find a drop in each of the distances
    Horrifically unoptimised
    distance_threshold, is how far shall it search to find prominence from peak
    prominence, is height from peak

    The prominence of a peak is the height of the peak’s summit above the lowest contour line encircling it but containing no higher summit within it.
    https://en.wikipedia.org/wiki/Topographic_prominence
    """
    # store
    prominent_peaks = []
    # work in directions
    directions = {}
    subtend = int(360 / angles)
    for i in range(angles):
        directions[i] = (np.sin(i), np.cos(i))

    # check each peak independantly
    for peak in peaks:
        # original point
        reference_point = (peak[1], peak[2])
        # no height can be higher
        height_threshold = peak[0]
        prominence_threshold = peak[0] - prominence
        contours_for_peak = []
        try:
            directs = dict([(d, False) for d in directions.keys()])
            # move outward
            for iteration in range(1, distance_threshold + 1):
                # in a spiral motion
                for direction, adjustments in directions.items():
                    # if not found threshold in that direction
                    if not directs[direction]:
                        y = reference_point[0] + \
                            int(adjustments[0] * iteration)
                        x = reference_point[1] + \
                            int(adjustments[1] * iteration)

                        check_height = surface[y][x]
                        # check not too high
                        if check_height > height_threshold:
                            raise BreakOut("Height threshold broken")
                        # is it deep enough
                        elif check_height < prominence_threshold:
                            directs[direction] = True
                            contours_for_peak.append((check_height, y, x))

                    # if found in all directions
                    if not False in directs.values():
                        prominent_peaks.append((peak, contours_for_peak))
                        raise BreakOut("Found peak!")
        except BreakOut:
            # if passed height of test peak, then fails test
            pass
        except IndexError:
            # if cannot find it without bounds then have assume is not
            pass
    return prominent_peaks


def distance_peaks(surface, locale=1, high_pass_filter=None):
    """
    Finds peaks highest first
    Ignores any other peaks 
    Sorted with heightest peaks first
    Dangerous as will find the highest point on the edge of a supplied distance as a peak
    find_peaks is a better algo
    No tests
    """
    dimension = common_surface_checks(surface, locale)

    # create list of all points
    points = []
    for index, height in np.ndenumerate(surface):
        # actively only include above certain height
        if high_pass_filter is None or height > high_pass_filter:
            # turn raw data into height, y, x
            points.append((height, *index))

    # create custom description
    dtype = [('height', int), ('y', int), ('x', int)]
    points = np.array(points, dtype=dtype)

    # descend based on
    sorted_points = np.sort(points, order='height')[::-1]

    i = 0
    length = len(sorted_points)
    while i < length:
        peak = sorted_points[i]
        # always start at the next one & review
        j = i + 1
        while j < length:
            # current review peak
            subpeak = sorted_points[j]

            # find distance between peaks
            dist = np.sqrt((peak[1] - subpeak[1])**2 +
                           (peak[2] - subpeak[2])**2)

            # if it's close, remove it
            if dist < locale:
                sorted_points = np.delete(sorted_points, j, 0)
                length -= 1
                j -= 1
            j += 1
        i += 1

    return sorted_points
