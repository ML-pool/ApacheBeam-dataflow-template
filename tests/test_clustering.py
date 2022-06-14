from .context import utils
import numpy as np

def test_sin():
    assert utils.sin(2) == np.sin(2)



