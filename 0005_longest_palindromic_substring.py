class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or s == ' ':
            return ''

        def cntr(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1:r]

        result = ''

        for i in range(len(s)):
            op = cntr(i, i)

            if len(op) > len(result):
                result = op

            ep = cntr(i, i + 1)
            if len(ep) > len(result):
                result = ep

        return result


if __name__ == '__main__':
    print(Solution().longestPalindrome("abcabcbb"))