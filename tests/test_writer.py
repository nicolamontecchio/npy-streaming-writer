import os
import shutil
import tempfile

import numpy as np
from npywriter import NpyWriter


def test_npywriter():
    """
    Test that the writer works by writing out random tensors with an
    NpyWriter, reading them back with numpy.load, and comparing them
    to their in-memory representation.
    """

    tmp_dir = tempfile.mkdtemp()
    output_fpath = os.path.join(tmp_dir, 'test.npy')

    test_array_seq = [np.random.randn(3,2,5) for _ in range(4)]

    writer = NpyWriter(output_fpath)
    for ta in test_array_seq:
        writer.append(ta)
    writer.close()

    assert np.sum(np.abs(
        np.load(output_fpath) - np.array(test_array_seq))) < 0.001

    shutil.rmtree(tmp_dir)
