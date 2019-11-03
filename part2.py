test = input("Input: ")
nums = test.split()

a = int(nums[0])
b = int(nums[1])

current = min(a,b)

ct =0

while(current > 0):
    current = current -1
    ct = ct + 1
    if(current > 0):
        current = current -2
        ct= ct+ 1

print(ct)