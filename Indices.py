class Indices():
    """
    Class implements emulation of nested loops through flattenning.
    Use it to generate indices to drive simulation. Simulation contains some
    parameters like temperature and deformation through which it evolves,
    preserving some order. One idea is to recursevely generate tuples with
    simulation parameters. But since recursive realization can be complex
    and program implemented in Python let's choose iterative realization.
    The idea is to build list-like structures with parameters and then
    generate tuples with indices that help fetch parameters for current
    simulation step.

    Little how to.
    Provide limits and starting element to constructor. Limits is set of max
    indices that need to be reached. Indices are inclusive. Current is starting
    element with all zeros by default. After that use class instance as 
    ordinary iterator.

    indices = Indices([2,1,3])
    for index in indices:
        print(index)

    Output:
    (0, 0, 0)
    (0, 0, 1)
    (0, 0, 2)
    (0, 0, 3)
    (0, 1, 0)
    (0, 1, 1)
    (0, 1, 2)
    (0, 1, 3)
    (1, 0, 0)
    (1, 0, 1)
    (1, 0, 2)
    (1, 0, 3)
    (1, 1, 0)
    (1, 1, 1)
    (1, 1, 2)
    (1, 1, 3)
    (2, 0, 0)
    (2, 0, 1)
    (2, 0, 2)
    (2, 0, 3)
    (2, 1, 0)
    (2, 1, 1)
    (2, 1, 2)
    (2, 1, 3)

    Also if all elements limits are zeros then ValueError exception raised.
    """
    def __init__(self, limits, current = None):
        if all(el == 0 for el in limits):
            raise ValueError('Limits values are all zero!')

        self.__limits = limits

        if current is not None:
            self.__current = current
        else:
            self.__current = [0] * len(self.__limits)

        self.__subsequent = self.__current[:]

    def __next_element(self):
        self.__current = self.__subsequent[:]
        for i, el in enumerate(self.__current[::-1]):
            if el < self.__limits[-1 - i]:
                self.__subsequent[-1 - i] += 1
                break
        if i > 0:
            self.__subsequent[-i:] = [0] * i

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current == self.__limits:
            raise StopIteration
        else:
            self.__next_element()
            return tuple(self.__current)
