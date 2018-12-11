def recip_square(i):
    return 1. / i**2

def approx_pi(n=1e7):
    val = 0.
    for i in range(1, int(n)):
        val += recip_square(i)
    return (6 * val) ** .5
