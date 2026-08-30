
# first name in reverse + space + lastname
full_name = 'Jaskirat Rangi'
firstname,lastname = full_name.split(' ')
print(firstname[len(firstname)::-1]+' '+lastname)
print(''.join(reversed(firstname))+' '+lastname)


# join
values = ['kale','lafi','zoro','nami','sanji','pickle']
print(';'.join(values))