# from python.org, http://docs.python.org/library/itertools.html
# the equivalent for itertools.combinations in a version of Python
# less than 2.6

def combinations(iterable, r):
    ''' combinations('ABCD', 2) --> AB AC AD BC BD CD
        combinations(range(4), 3) --> 012 013 023 123 
        La cantidad de combinaciones posibles es: N!/(N!*(N-r)!)
        donde N es la cantidad de elementos de iterable'''
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

# essentially 5 choose 2 combinations from a list
# since it is a generator, you have to explicitly iterate
# through all combinations

if __name__ == '__main__' :

	cantidad = 0

	for x in combinations(range(4), 3):
	    cantidad+=1
	    print (x)
	print("\nCantidad total de combinaciones: ",cantidad)
