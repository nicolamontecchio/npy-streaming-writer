from ctypes import create_string_buffer, c_uint8
import numpy as np


def is_allowed_type(item):
    if type(item) != np.ndarray:
        return False
    if item.dtype.type in [
            np.int8, np.int16, np.int32, np.int64,
            np.uint8, np.uint16, np.uint32, np.uint64,
            np.float16, np.float32, np.float64, np.float128]:
        return True
    return False


class NpyWriter:
    """
    An object to facilitate writing numerical data to disk, without
    the need for holding the whole data in memory at once at any point
    in time.

    Example usage:

        writer = NpyWriter('bigdata.npy')
        writer.append(np.array([1,2,3]))
        writer.append(np.array([4,5,6]))
        writer.close()

        np.load('bigdata.npy')
        > array([[1, 2, 3],
        >        [4, 5, 6]])

    Notes:

     - THE close() METHOD *MUST* BE CALLED otherwise the .npy file
       will be unreadable
     - the shape and type of the elements that get appended to the
       writer must be consistent, or a RuntimeError will occur
    """

    def __init__(self, output_fpath):
        self.output_fpath = output_fpath
        self.output_file = open(self.output_fpath, 'wb')
        for _ in range(128):
            self.output_file.write(" ")
        self.item_shape = None
        self.item_dtype = None
        self.n_items = 0

    def append(self, item):
        # check item type is a scalar o a numeric numpy array
        if not is_allowed_type(item):
            raise RuntimeError(
                'invalid type: must be a numeric type, either a scalar, a' +
                '(nested) list, or a numpy array')
        # is it the first item? this sets the shape ...
        if self.item_shape is None:
            self.item_shape = item.shape
            self.item_dtype = item.dtype
        # ... otherwise check the shape to make sure it matches the previous one
        else:
            if item.shape != self.item_shape:
                raise RuntimeError(
                    'item shape %s, does not match previous shape %s' % (
                        str(item.shape), str(self.latest_shape)))
            if item.dtype != self.item_dtype:
                raise RuntimeError(
                    'item type %s does not match previous type %s' % (
                        str(self.item_dtype), item.dtype))
        # - write binary blob to output in C order
        self.output_file.write(item.tobytes(order='C'))
        self.n_items += 1

    def close(self):
        # write header
        self.output_file.seek(0)
        self.output_file.write(c_uint8(147))
        self.output_file.write('NUMPY')
        self.output_file.write(c_uint8(1))
        self.output_file.write(c_uint8(0))
        self.output_file.write(c_uint8(118))   # uint16(118) in little endian
        self.output_file.write(c_uint8(0))     #
        total_shape = tuple([self.n_items] + list(self.item_shape))
        header = "{'descr': '%s', 'fortran_order': False, 'shape': %s}" % (
            self.item_dtype.descr[0][1], str(total_shape))
        self.output_file.write(header)
        self.output_file.close()
