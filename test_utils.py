from .utils import find_peaks, verify_prominence
import pytest

surface = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 60, 60, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 110],
]


def test_simple():

    # won't find 60 values, as not 'true' peaks
    # won't find 50 value as has partner 80 on edge
    # won't find 110 value as on edge
    # won't find 70 as 90 in range

    # defaults to 1 locale (i.e. 1 nearest neighbours)
    assert find_peaks(surface) == [(100, 3, 2), (90, 5, 2)]


def test_locale():

    # 90 inside it's locale 2 box range
    assert find_peaks(surface, locale=2) == [(100, 3, 2)]


def test_high_pass_filter():
    # high pass filter out 90 but keep 100
    assert find_peaks(surface, high_pass_filter=95) == [(100, 3, 2)]

    # high pass filter too high
    assert find_peaks(surface, high_pass_filter=105) == []


def test_errors():
    with pytest.raises(ValueError) as excinfo:
        find_peaks([])
    assert 'Surface cannot be null' in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        find_peaks(surface, locale=20)
    assert 'dimension too small' in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        find_peaks([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]],)
    assert "Surface must be a square" in str(excinfo)


def first(arr):
    return [a[0] for a in arr]

def test_threshold():
    peaks = find_peaks(surface)

    print(verify_prominence(surface, peaks, 10, 3))
    print(verify_prominence(surface, peaks, 3, 3))

    # doesn't find 90 as not prominent enough
    assert first(verify_prominence(surface, peaks, 10, 3)) == [(100, 3, 2)]
    # now lower prominence, will show
    assert first(verify_prominence(surface, peaks, 3, 3)) == [(100, 3, 2), (90, 5, 2)]

    # assert out of bounds
