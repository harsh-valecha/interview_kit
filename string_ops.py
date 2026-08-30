
# first name in reverse + space + lastname
full_name = 'Jaskirat Rangi'
firstname,lastname = full_name.split(' ')

# 3 ways to do it  - 
print(firstname[len(firstname)::-1]+' '+lastname)
print(firstname[::-1]+' '+lastname)
print(''.join(reversed(firstname))+' '+lastname)


# join
values = ['kale','lafi','zoro','nami','sanji','pickle']
print(';'.join(values))


# palindrome
val = 'racecar'
def is_palindrome(value):
    return value==value[::-1]
print(is_palindrome('racecar'))
print(is_palindrome('jethalal'))

# Remove duplicates from a string while preserving order
s = 'hululululujafar'
print(''.join(dict.fromkeys(s)))

# count occurences of characters in a string
from collections import Counter
print(Counter(s))

# Anagrams
def is_anagram(str1,str2):
    return Counter(str1.lower()) == Counter(str2.lower())

print(is_anagram('silent','listen'))
print(is_anagram('luffy','sanji'))

# Remove Spaces
str = '   KOOOOOL FULLTOOSH  '
print(str.lstrip()) # left space removing
print(str.rstrip()) # right space removing
print(str.strip()) # remove from both left and right 


# only digits in string
number = '987654321'
print(number.isdigit())


# first non repeating character in a string 
def first_unique(s):
    counts = Counter(s)
    for char in s:
        if counts[char]==1:
            return char
    return None

print(first_unique('jameeljamali'))

# check if a string starts with a prefix
print('Mr. Oliva'.startswith('Mr.'))

# starts with suffix
print('Baki Hanma'.endswith('Hanma'))