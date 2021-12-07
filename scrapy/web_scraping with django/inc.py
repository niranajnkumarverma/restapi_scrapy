def inc(x):
    print(x)
    if x < 20:
        x += 1
        inc(x)
        inc(1)
        