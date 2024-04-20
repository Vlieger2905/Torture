from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.core.node import Node
from pathfinding.finder.a_star import AStarFinder
from Making_Grid import *

matrix = tmx_to_grid("Map Data//Test Center//testMap.tmx")
# print(matrix)
# matrix = [[1,1,1,1,1],
#           [1,1,0,1,1],
#           [1,1,1,1,1]
#           ]

# 1. create the grid with the nodes 
grid = Grid(matrix=matrix)



# get start and end point 
start = grid.node(4, 4)
end = grid.node(8, 8)

# create a finder with the movement style 
finder = AStarFinder(diagonal_movement = DiagonalMovement.only_when_no_obstacle) # can add DiagonalMovement as argument here with never or always + more

# returns a list with the path and the amount of times the finder had to run to get the path 
path, runs = finder.find_path(start, end, grid)


temp = []
for point in path:
    position = point.x, point.y
    temp.append(position)

print(temp)
    

# print result  
# print(path)