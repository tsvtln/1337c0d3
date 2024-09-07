from math import ceil


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        val_col = 0
        listed_string = [st for st in s]

        if numRows == 1:
            val_row = len(s)
        else:
            val_row = numRows

        # if len(s) < 4 or numRows == 2:
        if len(s) % numRows < numRows:
            val_col = ceil(len(s) / 2)
        else:
            val_col = len(s) // 2

        mx = [['' for _ in range(val_col)] for _ in range(val_row)]


        for c in range(val_col):
            for rw in range(val_row):
                if listed_string:
                    if c==0 or c % (val_row-1) == 0:
                        mx[rw][c] = listed_string.pop(0)
                    else:
                        i = (val_row - 1) - c % (val_row - 1)
                        if rw != i:
                            continue
                        else:
                            mx[i][c] = listed_string.pop(0)



        res = []
        for row in range(val_row):
            for col in range(val_col):
                if mx[row][col]:
                    res.append(mx[row][col])


        return ''.join(res)
        # return mx



if __name__ == '__main__':
    res = Solution().convert("ABCDE", 3)
    for r in res:
        print(r)
    # print(res)
