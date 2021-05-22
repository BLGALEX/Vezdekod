import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# let's make half second tact

class RobotMoveGenerator:
    def __init__(self, length, bots):
        self.length = length
        self.bots = bots
        self.n = length * 2 + 1
        self.field = [' '] * self.n
        for bot, direction in bots:
            self.field[bot * 2] = ('>' if direction else '<')

    def next(self):
        field = [' '] * self.n
        for i in range(len(self.field)):
            to_left = (i != 0) and (self.field[i] == '<' or self.field[i] == 'X')
            to_right = (i != self.n - 1) and (self.field[i] == '>' or self.field[i] == 'X')

            if to_left:
                if field[i - 1] == '>':
                    field[i - 1] = 'X'
                else:
                    field[i - 1] = '<'
            if to_right:
                if field[i + 1] == '<':
                    field[i + 1] = 'X'
                else:
                    field[i + 1] = '>'

        self.field = field

    def has_next(self):
        return any(cell != ' ' for cell in self.field)

    def __str__(self):
        return "[" + ''.join(self.field) + "]"


length = int(input())
n = int(input())
bots = [(bot, bot * 2 < length) for bot in sorted(list(map(int, input().split())))]
gen = RobotMoveGenerator(length, bots)

def get_points(string : str):
    p = []
    c = []
    for i in range(len(string)):
        if string[i] == '>' or string[i] == '<':
            p.append([i/2, 0.5])
            c.append('r')
        elif string[i] == 'X':
            p.append([i/2, 0.5])
            c.append('maroon')
    return p, c



x = []
for i in bots:
    x.append(i[0])

fig = plt.figure()
ax = fig.add_subplot()

points = ax.scatter(x, np.zeros_like(x) + 0.5, marker="o", c='r', s=400)

ax.set_yticks([0, 1], )
ax.set_facecolor('gainsboro')
ax.set_xticks(np.arange(length + 1))
ax.set_xticks(np.arange(length + 2) - 0.5, minor=True)

ax.grid(True, which="minor")
ax.set_aspect("equal")
ax.tick_params(
    axis='y',
    left=False,
    labelleft=False)
plt.pause(1)
while gen.has_next():
    gen.next()
    gen.next()
    p, c = get_points(str(gen)[1:-1])
    points.set_offsets(p)
    points.set_color(c)
    plt.pause(1)
