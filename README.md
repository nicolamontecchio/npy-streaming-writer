npywriter
===============================

Overview
--------

A library for writing arbitrarily large .npy files incrementally.

Example Usage:
--------------

    from npywriter import NpyWriter
    
    writer = NpyWriter('bigdata.npy')
    writer.append(np.array([1,2,3]))
    writer.append(np.array([4,5,6]))
    writer.close()

    np.load('bigdata.npy')
    > array([[1, 2, 3],
    >        [4, 5, 6]])
