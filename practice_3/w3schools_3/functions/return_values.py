def count_followed_seq(s):
    counter = 0
    for i in range(1, len(s)):
        if s[i-1] == s[i]:
            counter += 1
    return counter

s = input()
result = count_followed_seq(s)
print(result)