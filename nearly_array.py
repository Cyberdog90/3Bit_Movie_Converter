def near(array, value):
    length = len(array)
    ans = 11451419198109318933349800364364
    for i in range(length):
        abans = abs(array[i] - int(value))
        if abans < ans:
            ans = abans
            ret = i

    return ret

#  main.py修正したらやる

"""
def near(array, value):
    length = len(array)
    ans = 11451419198109318933349800364364
    ret = []
    for i in range(length):
        abans = abs(array[i] - int(value))
        if abans < ans:
            ans = abans
            ret.append(array[i])
            ret.append(i)

    return ret

"""