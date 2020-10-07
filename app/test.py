list1 = [
  {'a': 'a1'},
  {'a': 'a2'}
]

print("before", list1)

for item in list1:
  item.update({'a': 'new_a'})

print("after", list1)