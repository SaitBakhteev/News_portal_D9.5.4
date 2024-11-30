import pytest
from for_tests import t, t1
def y():
    assert t(9)==True

def y1():
    assert t(2)==0

if __name__ == '__main__':
    pytest.main()