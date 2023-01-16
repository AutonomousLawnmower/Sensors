import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import numpy as np
from random import randint

path_points = [[0,2],[1, 7], [3, 9], [8,5], [5, 3], [1,1]]

path_x = []
path_y = []

for point in path_points:
  path_x.append(point[0])
  path_y.append(point[1])

path_x.append(path_points[0][0])
path_y.append(path_points[0][1])

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()

plt.plot(path_x, path_y)
plt.show()

exclusion_points = [[2,4],[2, 6], [4, 6], [6,4]]

exclusion_x = []
exclusion_y = []

for point in exclusion_points:
  exclusion_x.append(point[0])
  exclusion_y.append(point[1])

exclusion_x.append(exclusion_points[0][0])
exclusion_y.append(exclusion_points[0][1])

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()

plt.plot(exclusion_x, exclusion_y, color = 'red')
plt.show()

test_points = []
for i in range(10):
  test_points.append([randint(0,10), randint(0,10)])
  
poly_path = mplPath.Path(np.array(path_points))

for point in test_points: 
  print(point, "is in polygon:", poly_path.contains_point(point))
  
exclu_path = mplPath.Path(np.array(exclusion_points))

for point in test_points: 
  print(point, "is in polygon:", exclu_path.contains_point(point))
  
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid()

plt.plot(path_x, path_y)
plt.plot(exclusion_x, exclusion_y, linestyle='dashed', color='red')

for point in test_points:

  if poly_path.contains_point(point):
    point_color = 'green'
  else:
    point_color = 'red'
  if exclu_path.contains_point(point):
    point_color = 'red'

  plt.plot([point[0]], [point[1]], marker="o", linewidth=0, color=point_color)

plt.show()