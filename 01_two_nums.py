from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i, num in enumerate(nums):
            for i2, num2 in enumerate(nums):
                if i2 == i:
                    continue
                if num + num2 == target:
                    return [i, i2]



init_sol = Solution()
res = init_sol.twoSum([2,7,11,15], 9)

print(res)

