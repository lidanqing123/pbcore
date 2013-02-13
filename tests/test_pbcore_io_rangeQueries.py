from nose.tools import assert_equal
from numpy.testing import assert_array_equal

import pbcore.io.rangeQueries as RQ
from pbcore import data
from pbcore.io import CmpH5Reader

import bisect
from numpy import *

def brute_force_lm_search(vec, val):
    if (val not in vec):
        nvec = vec[ vec < val ]
        if (len(nvec) == 0):
            return(0)
        val = max(nvec)
    for i in range(0, len(vec)):
        if (vec[i] == val):
            break
    return(i)

def brute_force_rm_search(vec, val):
    if (val not in vec):
        nvec = vec[ vec > val ]
        if (len(nvec) == 0):
            return(len(vec))
        val = min(nvec)
        return(bisect.bisect_left(vec, val))
    else:
        return(bisect.bisect_right(vec, val) - 1)

class TestRightmostBinSearch:
    def test_rightmost_bin_search(self):
        for j in range(0, 100):
            a = sort(random.randint(0, 100, 100))
            v = random.randint(0, 100, 1)
            assert_equal(RQ.rightmostBinSearch(a, v), brute_force_rm_search(a, v))

class TestLeftmostBinSearch:
    def test_leftmost_bin_search(self):
        for j in range(0, 100):
            a = sort(random.randint(0, 100, 100))
            v = random.randint(0, 100, 1)
            assert_equal(RQ.leftmostBinSearch(a, v),
                         brute_force_lm_search(a, v))

class TestProjectIntoRange:
    def test_project_into_range(self):
        tStart = array([1,1,1,1,1,2,2,2,2,10,20])
        tEnd   = array([2,3,4,5,6,3,4,5,6,15,25])
        assert_equal(True, all(RQ.projectIntoRange(tStart, tEnd, 1, 5) == array([5, 8, 6, 4, 2])))
        assert_equal(True, all(RQ.projectIntoRange(tStart, tEnd, 20, 25) == array([1, 1, 1, 1, 1, 0])))

def brute_force_reads_in_range(rangeStart, rangeEnd, tStart, tEnd):
    mask = ((tEnd   > rangeStart) &
            (tStart < rangeEnd))
    return flatnonzero(mask)

class TestGetReadsInRange:
    def __init__(self):
        self.h5FileName = data.getCmpH5()['cmph5']
        self.cmpH5 = CmpH5Reader(self.h5FileName)

    def test_get_reads_in_range(self):
        assert(len(RQ.getReadsInRange(self.cmpH5, (1, 0, 100000), justIndices = True)) == 84)

    def test_get_coverage_in_range(self):
        assert(all(RQ.getCoverageInRange(self.cmpH5, (1, 0, 100)) == 2))

    def test_reads_in_range2(self):
        # This is a brute force check that reads in range returns the
        # right answer for 50-base windows of lambda
        for winStart in xrange(0, 45000, 50):
            winEnd = winStart + 50
            assert_array_equal(brute_force_reads_in_range(winStart, winEnd, self.cmpH5.tStart, self.cmpH5.tEnd),
                               self.cmpH5.readsInRange(1, winStart, winEnd-1, justIndices=True))
