from random import choice
from numpy import full


def generate_image(map_):
    for number in range(len(map_)):
        for x in range(len(map_[-1])):
            if map_[number][x] == (0, 0, 0):
                map_[number][x] = (255, 255, 255)
            if map_[number][x] == -1:
                map_[number][x] = (0, 255, 0)

            else:
                map_[number][x] = 1
    return map_


def generate_random_n_p_n_matrix(n):
    return full((n, n), -1)


def get_coordenates(map_):
    for y in range(len(map_)):
        for x in range(len(map_[-1])):
            yield [x, y]


class QuickFind:
    def __init__(self):
        self.values = []
        self.ids = []
        self.connection_groups = []

    def union(self, x, y):
        if x not in self.values:
            self.values.append(x)
            self.ids.append(x)
        if y not in self.values:
            self.values.append(y)
            self.ids.append(y)
        self.ids[self.values.index(y)] = x

        n_groups = [number for number in range(len(self.connection_groups)) if
                    (x in self.connection_groups[number] or y in self.connection_groups[number])]

        new_group = [x, y]
        old_groups = []
        for number in n_groups:
            new_group += self.connection_groups[number].copy()
            old_groups.append(self.connection_groups[number].copy())
        if len(new_group) > 2:
            for group in old_groups:
                self.connection_groups.remove(group)
            self.connection_groups.append(list(set(new_group)))
            self.connection_groups.sort(key=len)
            return
        self.connection_groups.append([x, y])

    def root(self, x):
        for group in self.connection_groups:
            if x in group:
                for value in group:
                    if self.ids[self.values.index(value)] == value:
                        yield value

    def connected(self, x, y):
        for group in self.connection_groups:
            if x in group:
                if y in group:
                    return True
        return False


class Percolation:
    def __init__(self, map_, blocks):
        # The actual map
        self.map = map_
        self.blocks = blocks

        # Reference of values in x,y
        self.reference = list(get_coordenates(self.map))

        self.open_ports = []

        self.blocks_closed = self.reference.copy()

        self.quickwind = QuickFind()

        self.__randomize()

    def __near(self, block):
        return list(filter(lambda x: x in self.open_ports and -1 not in x and x[0] < len(self.map[-1]) and x[1] < len(self.map),
                           [[block[0]-1, block[1]], [block[0], block[1]-1], [block[0]+1, block[1]], [block[0], block[1]+1]]))

    def __randomize(self):
        for block in range(self.blocks):
            block = choice(self.blocks_closed)
            self.map[block[1]][block[0]] = self.reference.index(block)
            self.open_ports.append(block.copy())
            self.blocks_closed.remove(block.copy())

    def __solver(self,block):
        b_coor = self.reference.index(block)
        for possible in self.__near(block):
            self.quickwind.union(b_coor, self.reference.index(possible))
    def __solve_perlocation(self):
        for block in self.open_ports:
            self.__solver(block)
        for value in self.map[-1]:
            if value not in [0,-1]:
                for v in self.map[0]:
                    if self.quickwind.connected(value,v):
                        return True
        return False

    def solve(self):
        self.__solve_perlocation()
        for value in self.map[-1]:
            if value not in [0,-1]:
                for v in self.map[0]:
                    if self.quickwind.connected(value,v):
                        return True
        return False

from time import time
map_ = generate_random_n_p_n_matrix(5)
print("Generating map")
t = time()
p = Percolation(map_, 15)
print('Map generated in',time()-t)
print('Solving')
t = time()
s = p.solve()
print("Solved in",time()-t)
print(s)
# 0.015
