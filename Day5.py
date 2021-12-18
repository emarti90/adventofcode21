'''
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
'''
import pandas as pd
import numpy as np

df = pd.read_csv("Day5.txt", sep=" -> |,", header=None, names=['X1','Y1','X2','Y2'], engine='python')

vents = df.apply(pd.to_numeric)

Xmax = max(vents['X1'].append(vents['X2']))
Ymax = max(vents['Y1'].append(vents['Y2']))
diag = np.zeros((Xmax+1,Ymax+1),dtype=np.int)

for i in range(len(vents)):
    x1 = vents['X1'].iloc[i]
    y1 = vents['Y1'].iloc[i]
    x2 = vents['X2'].iloc[i]
    y2 = vents['Y2'].iloc[i]
    if x1 == x2: # Vertical
        x = x1
        if y1 > y2:
            y2 = vents['Y1'].iloc[i]
            y1 = vents['Y2'].iloc[i]
        for y in np.arange(y1,y2+1):
            diag[x][y] += 1
    if y1 == y2: # Horiz
        y = y1
        if x1 > x2:
            x2 = vents['X1'].iloc[i]
            x1 = vents['X2'].iloc[i]
        for x in np.arange(x1,x2+1):
            diag[x][y] += 1

danger = len(np.where(diag >= 2)[0])

print(danger)

'''
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
'''

diag = np.zeros((Xmax+1,Ymax+1),dtype=np.int)

for i in range(len(vents)):
    x1 = vents['X1'].iloc[i]
    y1 = vents['Y1'].iloc[i]
    x2 = vents['X2'].iloc[i]
    y2 = vents['Y2'].iloc[i]

    Xdiff = x2 - x1
    Ydiff = y2 - y1

    if Xdiff == 0: # Vertical
        x = x1
        if y1 > y2:
            y2 = vents['Y1'].iloc[i]
            y1 = vents['Y2'].iloc[i]
        for y in np.arange(y1,y2+1):
            diag[y][x] += 1

    elif Ydiff == 0: # Horiz
        y = y1
        if x1 > x2:
            x2 = vents['X1'].iloc[i]
            x1 = vents['X2'].iloc[i]
        for x in np.arange(x1,x2+1):
            diag[y][x] += 1

    elif (Xdiff == Ydiff) and (Xdiff > 0): # Diagonal ↗
        for i in range(Xdiff+1):
            diag[y1+i][x1+i] += 1
        
    elif (Xdiff == Ydiff) and (Xdiff < 0): # Diagonal ↙
        for i in range(abs(Xdiff)+1):
            diag[y1-i][x1-i] += 1
    elif Xdiff > Ydiff: # Diagonal ↘
        for i in range(Xdiff+1):
            diag[y1-i][x1+i]
    elif Xdiff < Ydiff:
        for i in range(Ydiff+1): # Diagonal ↖
            diag[y1+i][x1-i]

danger = len(np.where(diag >= 2)[0])

print(danger)
