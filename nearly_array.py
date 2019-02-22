def near(array, value):
    length = len(array)
    ans = 11451419198109318933349800364364
    for i in range(length):
        abans = abs(array[i] - int(value))
        if abans < ans:
            ans = abans
            ret = i

    return ret
