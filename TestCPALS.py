import unittest
import CPALS

# I need to modify this module to run.

class TestCPALS(unittest.TestCase):
    def __init__(self):
        self.dim_list = [3,3,3]
        self.rank = 10
        self.CPALS = CPALS.CPALS(self.dim_list, self.rank)

    def test_make_init_factor_matrix(self, dim, rank):
        fmat = self.CPALS._make_init_factor_matrix(self.dim_list[0], self.rank)
        assert fmat is not None

if __name__ == '__main__':
    testcpals = TestCPALS()
    # python -m unittest TestCPALS.py
