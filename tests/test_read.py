import numpy as np
import pytest
import segyio

from pyzgy.read import SeismicReader
from openzgy.exception import ZgyUserError


def test_read_ilines_list(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert np.all(reader.ilines == sgyfile.ilines)


def test_read_xlines_list(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert np.all(reader.xlines == sgyfile.xlines)


def test_read_samples_list(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert np.all(reader.samples == sgyfile.samples)


def test_read_ilines_datatype(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert reader.ilines.dtype == sgyfile.ilines.dtype
        assert reader.ilines.ndim == 1


def test_read_xlines_datatype(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert reader.xlines.dtype == sgyfile.xlines.dtype
        assert reader.xlines.ndim == 1


def test_read_samples_datatype(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    reader = SeismicReader(ZGY_FILE)
    with segyio.open(SGY_FILE) as sgyfile:
        assert reader.samples.dtype == sgyfile.samples.dtype
        assert reader.samples.ndim == 1


def compare_inline(zgy_filename, sgy_filename, lines, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for line_number in range(lines):
            slice_zgy = reader.read_inline(line_number)
            slice_segy = segyfile.iline[segyfile.ilines[line_number]]
        assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)


def compare_inline_number(zgy_filename, sgy_filename, line_coords, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for line_number in line_coords:
            slice_zgy = reader.read_inline_number(line_number)
            slice_segy = segyfile.iline[line_number]
        assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)
        assert slice_zgy.ndim == 2


def test_read_inline(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_inline(ZGY_FILE, SGY_FILE, 5, tolerance=1e-5)
    compare_inline_number(ZGY_FILE, SGY_FILE, [1, 2, 3, 4, 5], tolerance=1e-5)


def compare_crossline(zgy_filename, sgy_filename, lines, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for line_number in range(lines):
            slice_zgy = reader.read_crossline(line_number)
            slice_segy = segyfile.xline[segyfile.xlines[line_number]]
        assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)
        assert slice_zgy.ndim == 2


def compare_crossline_number(zgy_filename, sgy_filename, line_coords, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for line_number in line_coords:
            slice_zgy = reader.read_crossline_number(line_number)
            slice_segy = segyfile.xline[line_number]
        assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)
        assert slice_zgy.ndim == 2


def test_read_crossline(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_crossline(ZGY_FILE, SGY_FILE, 5, tolerance=1e-5)
    compare_crossline_number(ZGY_FILE, SGY_FILE, [20, 21, 22, 23, 24], tolerance=1e-5)


def compare_zslice(zgy_filename, sgy_filename, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for line_number in range(50):
            slice_zgy = reader.read_zslice(line_number)
            slice_segy = segyfile.depth_slice[line_number]
            assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)

def compare_zslice_coord(zgy_filename, sgy_filename, tolerance):
    with segyio.open(sgy_filename) as segyfile:
        reader = SeismicReader(zgy_filename)
        for slice_coord, slice_index in zip(range(0, 200, 4), range(50)):
            slice_zgy = reader.read_zslice_coord(slice_coord)
            slice_segy = segyfile.depth_slice[slice_index]
            assert np.allclose(slice_zgy, slice_segy, rtol=tolerance)


def test_read_zslice(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_zslice(ZGY_FILE, SGY_FILE, tolerance=1e-5)
    compare_zslice_coord(ZGY_FILE, SGY_FILE,  tolerance=1e-5)


def compare_subvolume(zgy_filename, sgy_filename, tolerance):
    min_il, max_il = 2,  3
    min_xl, max_xl = 1,  2
    min_z,  max_z = 10, 20
    vol_zgy = SeismicReader(zgy_filename).read_subvolume(min_il=min_il, max_il=max_il,
                                                     min_xl=min_xl, max_xl=max_xl,
                                                     min_z=min_z, max_z=max_z)
    vol_segy = segyio.tools.cube(sgy_filename)[min_il:max_il, min_xl:max_xl, min_z:max_z]
    assert np.allclose(vol_zgy, vol_segy, rtol=tolerance)


def test_read_subvolume(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_subvolume(ZGY_FILE, SGY_FILE, tolerance=1e-5)


def compare_volume(zgy_filename, sgy_filename, tolerance):
    vol_zgy = SeismicReader(zgy_filename).read_volume()
    vol_segy = segyio.tools.cube(sgy_filename)
    assert np.allclose(vol_zgy, vol_segy, rtol=tolerance)


def test_read_volume(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_volume(ZGY_FILE, SGY_FILE, tolerance=1e-5)


def test_file_close(zgy_sgy_file_pairs):
    with pytest.raises(ZgyUserError):
        zgy_filename, _ = zgy_sgy_file_pairs
        zgy_file = SeismicReader(zgy_filename)
        zgy_file.close()
        zgy_file.read_volume()


def compare_trace_header(zgy_filename, sgy_filename):
    reader = SeismicReader(zgy_filename)
    with segyio.open(sgy_filename) as sgyfile:
        for trace_number in range(25):
            sgz_header = reader.gen_trace_header(trace_number)
            sgy_header = sgyfile.header[trace_number]
            for pos in [181, 185]:
                assert sgz_header[pos] == sgy_header[pos]


def test_read_trace_header(zgy_sgy_file_pairs):
    ZGY_FILE, SGY_FILE = zgy_sgy_file_pairs
    compare_trace_header(ZGY_FILE, SGY_FILE)
