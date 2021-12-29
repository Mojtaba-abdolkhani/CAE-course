import math
data = open("input.txt","r").readlines()
A = list()
B = list()
for satr in data:
 if satr != '\n':
  nums = satr.split()
  A.append(float(nums[0]))
  B.append(float(nums[1]))
print(A)
print(B)
integ=0
i=0
while i < len(A) - 1:
 integ = integ + ( math.exp(B[i])*(A[i+1] - A[i]) )
 i=i+1
print(integ)
