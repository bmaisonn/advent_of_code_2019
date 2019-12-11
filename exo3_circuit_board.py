from copy import deepcopy
import numpy as np

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def distance_from_origin(self):
        return abs(self.x) + abs(self.y)

    def move(self, direction):
        if direction == 'U':
            self.y += 1
        elif direction == 'D':
            self.y -= 1
        if direction == 'R':
            self.x += 1
        if direction == 'L':
            self.x -= 1

class Board:
    def __init__(self):
        self.matrix = np.zeros((40000, 40000))

    @classmethod
    def transform_point(cls, p):
        x = p.x + 20000 if p.x > 0 else -p.x
        y = p.y + 20000 if p.y > 0 else -p.y
        return (x,y)


    def mark(self, p, distance):
        x,y = Board.transform_point(p)
        self.matrix[x][y] = distance

    def is_marked(self, p):
        x,y = Board.transform_point(p)
        return self.matrix[x][y] > 0
    
    def get_distance(self, p):
        x,y = Board.transform_point(p)
        return self.matrix[x][y]


def find_intersections(path1, path2):
    circuit_board = Board()

    p = Point()

    distance = 0

    for move in path1:
        direction = move[0]
        length = int(move[1:])

        for _ in range(length):
            p.move(direction)
            distance += 1
            circuit_board.mark(p, distance)

    intersections = []
    p = Point()

    distance = 0

    for move in path2:
        direction = move[0]
        length = int(move[1:])

        for _ in range(length):
            p.move(direction)
            distance += 1
            if circuit_board.is_marked(p):
                first_distance = circuit_board.get_distance(p)
                intersections.append(distance+first_distance)

    intersections = sorted(intersections)

    return None if not intersections else intersections[0]

def build_paths(path):
    with open(path) as f:
        path1 = f.readline().split(',')
        path2 = f.readline().split(',')
        return path1, path2

if __name__ == '__main__':

    path1, path2 = build_paths('exo31.txt')

    intersection = find_intersections(path1, path2)

    if intersection:
        print(intersection)