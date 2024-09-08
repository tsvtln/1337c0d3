# 45ms
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        num = x * sign
        num = int(''.join(map(str, reversed(str(num))))) * sign
        if num < -2**31 or num > 2**31 - 1:
            return 0
        return num


# print(Solution().reverse(321))

# 11ms
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        res = 0
        n = abs(x)
        while n != 0:
            res = res * 10 + n % 10
            if res > 2 ** 31 - 1:
                return 0
            n //= 10

        return res * sign