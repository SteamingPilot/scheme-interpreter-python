import os
import sys
import pytest
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.

sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

from interp import interpret

def test_let9():
    with pytest.raises(RuntimeError):
        interpret("(let ((x 3) (y 7) (z 9) (y 3)) #t)")