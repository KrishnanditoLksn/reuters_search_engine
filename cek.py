"""Two pointer pattern """
from typing import List


def twopointer(arr, target):
    left = 0
    right = len(arr) - 1
    indexed_nums = [(arr[i], i) for i in range(len(arr))]
    indexed_nums.sort()
    print(indexed_nums)

    while left < right:
        currentsum = indexed_nums[left][0] + indexed_nums[right][0]

        if currentsum == target:
            return [indexed_nums[left][1], indexed_nums[right][1]]

        if currentsum < target:
            left += 1

        else:
            right -= 1

    return []


def twoSum(self, nums: List[int], target: int) -> List[int]:
    left = 0
    right = len(nums) - 1

    while left < right:
        currentsum = nums[left] + nums[right]

        if currentsum == target:
            return [left, right]

        if currentsum < target:
            left += 1

        elif currentsum > target:
            right -= 1

    return [-1, -1]


if __name__ == '__main__':
    print(twopointer([2, 3, 4], 5))
