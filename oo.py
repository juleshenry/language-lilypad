list1 = [1, 2, 3, 4, 5, 6, 7, 8]
list2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

result = list(zip(list1[::2], list2[1::2]))

print(result)