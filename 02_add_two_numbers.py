# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
from typing import Optional


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # l1r = l1[::-1]
        # l2r = l2[::-1]
        # l1s = ''
        # l2s = ''
        # for n in l1r:
        #     l1s += str(n)
        # for n in l2r:
        #     l2s += str(n)
        #
        # res = str(int(l1s) + int(l2s))[::-1]
        # tp = []
        #
        # for item in res:
        #     tp.append(int(item))
        #
        # return tp

        dummy_head = ListNode(0)
        current = dummy_head
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            result = val1 + val2 + carry
            carry = result // 10
            current.next = ListNode(result % 10)

            current = current.next
            if l1: l1 = l1.next
            if l2: l2 = l2.next

        return dummy_head.next

sol = Solution()
pp = sol.addTwoNumbers(l1 = [2,4,3], l2 = [5,6,4])
print(pp)




