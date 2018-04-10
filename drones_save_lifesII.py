# Import the skfmm package as the library solving the problem
import skfmm
import numpy as np
import matplotlib.pyplot as plt
import time # Record the excution time
import warnings
import os
# Initialize global parameters
map_length = 20
warnings.filterwarnings("ignore")
# Function take the coordinates and radius as inputs and install the map
def drone_saves_life(centroid_x, centroid_y, radius, num_grid, image_path):
    # start_time = time.time()
    # Create a mask map to template the shortest path
    grid_map = np.ones((num_grid+1, num_grid+1))
    mask = np.full(np.shape(grid_map), False, dtype=bool)
    coordinate_x = centroid_x/map_length * num_grid
    coordinate_y = centroid_y/map_length * num_grid
    for i in range(num_grid+1):
        for j in range(num_grid+1):
            if radius/map_length * num_grid >= np.sqrt((i - coordinate_x)**2 + (j - coordinate_y)**2) :
                mask[i,j] = True
    # Creating two grid maps based on the position of point A and point B
    # We also want to nullify the points on the grid that has been marked as the storm area
    grid_map_A  = np.ma.MaskedArray(np.ones((num_grid+1, num_grid+1)), mask)
    grid_map_B  = np.ma.MaskedArray(np.ones((num_grid+1, num_grid+1)), mask)
    # Mark off the start and end point:
    grid_map_A[0, 0] = 0
    grid_map_B[num_grid, num_grid] = 0
    # Then we could use the skfmm to solve the traveling time for us 
    dist_map_A = skfmm.travel_time(grid_map_A, np.ones_like(grid_map), dx = map_length / num_grid)
    dist_map_B = skfmm.travel_time(grid_map_B, np.ones_like(grid_map), dx = map_length / num_grid)
    shortest_distance = dist_map_A[num_grid, num_grid]
    # print('The shortest distance is :' + str(shortest_distance))
    # We could obtain the shortest path
    shortest_path = finding_shortest_path(dist_map_A, dist_map_B, num_grid)
    path_visualization_and_save(centroid_x, centroid_y, radius, shortest_path, image_path)
    # computation_time = time.time() - start_time
    # print("The compution time is (unit:sec) :" + str(computation_time))
    return shortest_distance
   # Finding the shortest path
def finding_shortest_path(dist_map_A, dist_map_B, num_grid):
    # Initialize an empty array to store the shortest path
    shortest_path = []
    # Aggregate two distance maps so that we could determine if some point is on the shortest path
    global_dist_map = dist_map_A + dist_map_B
    # Two incrementing variables indicating the coordinates of current position and the next step:
    # Initialize them as the start point
    a, b = 0, 0
    while not (a == num_grid and b == num_grid):
        coordinate_a = a/num_grid*map_length
        coordinate_b = b/num_grid*map_length
        # Append the current coordinates in the shortest path:
        shortest_path.append([coordinate_a, coordinate_b])
        distance = 400
        next_step = [-1,-1]
        # There are three potential way to choose the next step
        for next_a, next_b in [[a+1, b], [a, b+1], [a+1, b+1]]:
            if  next_a <= num_grid and next_b <= num_grid and global_dist_map[next_a][next_b] < distance:
                # Update the distance information and the next step coordinates
                distance = global_dist_map[next_a][next_b]
                next_step = [next_a, next_b]
        a = next_step[0]
        b = next_step[1]
    # Append the end to the shortest path:
    shortest_path.append([map_length, map_length])  
    return shortest_path
 # Visualize the path:
def path_visualization_and_save(centroid_x, centroid_y, radius, shortest_path, image_path):
    # Plot the Storm Area:
    storm_area = plt.Circle((centroid_x, centroid_y), radius, color='yellow')
    # np array the shortest path:
    np_path = np.array(shortest_path)
    # Get the instance of the current axes
    axes = plt.gca()
    axes.add_patch(storm_area)
    # Plot the path:
    path_plot = plt.plot(*np_path.T, color = 'black')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    # plt.show()
    # If there is already a file at the path, we gonna replace it with the new file
    if os.path.isfile(image_path):
        os.remove(image_path)
    plt.savefig(image_path)
    plt.close('all')