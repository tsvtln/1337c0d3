import statistics
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        combined_list = nums1 + nums2
        combined_list.sort()
        return float("{:.5f}".format(statistics.median(map(float, combined_list))))


if __name__ == "__main__":
    print(Solution().findMedianSortedArrays(nums1=[1, 2], nums2=[1, 2]))
