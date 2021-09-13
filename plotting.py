import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


x, y = [], []
with open('commit_char_cnts.csv') as file:
    for i, line in enumerate(file.readlines()):
        time_part, cnt_part = line.split(', ')[1], line.split(', ')[2]
        commit_time = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S')
        cnt = int(cnt_part)
        if i == 0:
            t0 = commit_time

        x.append((t0-commit_time).days)
        y.append(cnt)

x = np.array(x)
y = np.array(list(reversed(y)))

print('first commit:', commit_time)
print('last commit:', t0)
print('time between first and last commit:', (t0-commit_time).days)
chars_per_page = 3000  # assumed characters per page...

plt.plot(x, y/chars_per_page)
plt.xlabel('time (days)')
plt.ylabel('~ accumulated pages')
plt.show()

y = np.diff(y)

plt.plot(x[1:], y/chars_per_page)
plt.xlabel('time (days)')
plt.ylabel('~ page differences')
plt.show()

