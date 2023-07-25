import
""" This program has been adapted for use by GVAHIM
       - the main revisions regard pep8 compliance and use of variable names

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0


Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Basic list exercises
Fill in the code for the functions below. main() is already set up
to call the functions with a few different inputs,
printing 'OK' when each function is correct.
The starter code for each function includes a 'return'
which is just a placeholder for your code.
It's ok if you do not complete all the functions, and there
are some additional functions to try in list2.py. """


# A. match_ends
# Given a list of strings, return the count of the number of
# strings where the string length is 2 or more and the first
# and last chars of the string are the same.
# Note: python does not have a ++ operator, but += works.

""" a func that get a list of strings and count the number of words in it that start and end withe the same letter"""
def match_ends(words):
    counter = 0
    for s in words: # a loop of all the words
        if len(s) >= 2:
            if s[0] == s[-1]:
                counter += 1
    return counter


# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.

""" a func that sort the words of a given list' words that start with 'x' first"""
def front_x(words):
    listx = []
    list2 = []
    for s in words: # a loop that sort the list into to list - one start with 'x'
        if s.startswith('x'):
            listx.append(s)
        else:
            list2.append(s)
    listx.sort()
    list2.sort()
    for s in list2: # a loop that combine the 2 lists
        listx.append(s)
    return listx


# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.


def extract_last (tuples): # a key func that return the last num in the tuple
    return tuples[-1]

"""a func that sort the tuples list by the value of the last val in ach tuple"""
def sort_last(tuples):
    tuples.sort(key = extract_last) # sort the list with the key func
    return tuples


# D. Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.

"""a func that remove adjacent equal values in a list  """
def remove_adjacent(nums):
    length = len(nums)
    i = 0
    while i < (length-1):
        if i == (length-1):
            break
        elif nums[i] == nums[i+1]:
                nums.pop(i)
                length -= 1
                i -= 1
        i += 1
    return nums


# E. Given two lists sorted in increasing order, create and return a merged
# list of all the elements in sorted order. You may modify the passed in lists.
# Ideally, the solution should work in "linear" time, making a single
# pass of both lists.
#
# NOTE - DO NOT use return sorted(sorted1 + sorted2) - that's too easy :-)
#

""" a func that combine and sort to sorted list in linear time"""
def linear_merge(sorted1, sorted2):
    res = []
    while(sorted1 and sorted2): # a loop that run until both list aren't empty
            if sorted1[0] < sorted2[0]:
                res.append(sorted1.pop(0))
            else:
                res.append(sorted2.pop(0))
    sorted1.extend(sorted2)
    res.extend(sorted1)
    return res


def test(got, expected):
    """ simple test() function used in main() to print
        what each function returns vs. what it's supposed to return. """

    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


def main():
    """ main() calls the above functions with interesting inputs,
        using test() to check if each result is correct or not. """

    print('\nmatch_ends')
    test(match_ends(['aba', 'xyz', 'aa', 'x', 'bbb']), 3)
    test(match_ends(['', 'x', 'xy', 'xyx', 'xx']), 2)
    test(match_ends(['aaa', 'be', 'abc', 'hello']), 1)

    print('\nfront_x')
    test(front_x(['bbb', 'ccc', 'axx', 'xzz', 'xaa']),
         ['xaa', 'xzz', 'axx', 'bbb', 'ccc'])
    test(front_x(['ccc', 'bbb', 'aaa', 'xcc', 'xaa']),
         ['xaa', 'xcc', 'aaa', 'bbb', 'ccc'])
    test(front_x(['mix', 'xyz', 'apple', 'xanadu', 'aardvark']),
         ['xanadu', 'xyz', 'aardvark', 'apple', 'mix'])

    print('\nsort_last')
    test(sort_last([(1, 3), (3, 2), (2, 1)]),
         [(2, 1), (3, 2), (1, 3)])
    test(sort_last([(2, 3), (1, 2), (3, 1)]),
         [(3, 1), (1, 2), (2, 3)])
    test(sort_last([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
         [(2, 2), (1, 3), (3, 4, 5), (1, 7)])

    print('\nremove_adjacent')
    test(remove_adjacent([1, 2, 2, 3]), [1, 2, 3])
    test(remove_adjacent([1, 3, 3, 2, 2, 3]), [1, 3, 2, 3])
    test(remove_adjacent([2, 2, 3, 3, 3]), [2, 3])
    test(remove_adjacent([]), [])

    print('\nlinear_merge')
    test(linear_merge(['aa', 'xx', 'zz'], ['bb', 'cc']),
         ['aa', 'bb', 'cc', 'xx', 'zz'])
    test(linear_merge(['aa', 'xx'], ['bb', 'cc', 'zz']),
         ['aa', 'bb', 'cc', 'xx', 'zz'])
    test(linear_merge(['aa', 'aa'], ['aa', 'bb', 'bb']),
         ['aa', 'aa', 'aa', 'bb', 'bb'])


if __name__ == '__main__':
    main()