import numpy as np

def angle_maker(angle, r, ref_x=0, ref_y=0):
    points = []
    for i in range(int(360/angle)):
        x = r*np.sin(i)
        y = r*np.coh(i)

    return x, y



def verify_prominence(surface, peaks, prominence, distance_threshold, angles):
    """
    Key assumption is if can find a drop in each of the distances
    Horrifically unoptimised
    distance_threshold, is how far shall it search to find prominence from peak
    prominence, is height from peak

    The prominence of a peak is the height of the peak’s summit above the lowest contour line encircling it but containing no higher summit within it.
    https://en.wikipedia.org/wiki/Topographic_prominence
    """
    # order peaks by heighest (as most interesting)
    prominent_peaks = []
    directions = {
        'n':  (-1, 0),
        'ne': (-1, 1),
        'e':  (0, 1),
        'se': (1, 1),
        's':  (1, 0),
        'sw': (1, -1),
        'w':  (0, -1),
        'nw': (-1, -1),
    }
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
            for iteration in range(1,distance_threshold+1):
                # in a spiral motion
                for direction, adjustments in directions.items():
                    # if not found threshold in that direction
                    if not directs[direction]:
                        y = reference_point[0] + adjustments[0] * iteration
                        x = reference_point[1] + adjustments[1] * iteration

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
    return prominent_peaks, contour_points






