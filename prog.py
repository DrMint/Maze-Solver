import pygame

class Point:
    ''' Is a point with 2 coordonates.'''

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'x = ' + str(self.x) + ' y = ' + str(self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def tuple(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def find_color(surface, color):
    ''' Find a pixel with a particular color in a surface
        Returns the coordonates of that pixel or Point(-1,-1) if not found.'''
    
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if surface.get_at((x, y)) == color:
                return Point(x,y)
    return Point(-1,-1)


def next_color(color):
    ''' For a color, give the next color in the series.
        The series goes as follow: Green, Blue, Red and then Green again.
        e.g (0,255,0) then (0,254,1) then (0,253,2) until (0,0,255) then (1,0,254)...'''
    
    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]
    
    if r > 0 and b == 0:
        r -= 1
        g += 1
    elif g > 0 and r == 0:
        g -= 1
        b += 1
    else:
        b -= 1
        r += 1
    return (r, g, b, a)

def previous_color(color):
    ''' Same thing as next_color but in reverse order.
        It returns the previous element in the series'''
    
    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]
    
    if g > 0 and b == 0:
        g -= 1
        r += 1
    elif r > 0 and g == 0:
        r -= 1
        b += 1
    else:
        b -= 1
        g += 1
    return (r, g, b, a)


def expand():
    ''' For each pixel in the list of coordonates (points), try to expand this list in all direction.
        Once all valid neighboor pixels as been added to the list, remove the current pixel from said list.
        If the ending color is detected, put its coordonnates in path_current, and change the state from 0 to 1.'''
    
    global points, path_current, end

    up = Point(0,1)
    down = Point(0,-1)
    left = Point(-1,0)
    right = Point(1,0)

    directions = [up, down, left, right]
    
    for point in points:
        color = next_color(maze.get_at(point.tuple()))
        for neighboor in [point + direction for direction in directions]:

            # I used try and except instead of properly accounting for the maze's borders.
            try:
                if maze.get_at(neighboor.tuple()) == white:
                    maze.set_at(neighboor.tuple(), color)
                    points += [neighboor]
                elif neighboor == end:
                    path_current = point
                    return 1
            except:
                pass
                
        points.remove(point)
        
    return 0


def path():
    ''' Is used in state 2 of the program. Draws the path to take from
        the ending point to the starting point in the color yellow.'''
    
    global path_current, result_lenght, start

    result_lenght += 1
    current_color = maze.get_at(path_current.tuple())
    point_color = previous_color(current_color)
    maze.set_at(path_current.tuple(), yellow)

    # If path_current is the start, changes the current state from 1 to 2.
    if path_current == start: return 2

    up = Point(0,1)
    down = Point(0,-1)
    left = Point(-1,0)
    right = Point(1,0)

    directions = [up, down, left, right]

    for neighboor in [path_current + direction for direction in directions]:
        if maze.get_at(neighboor.tuple()) == point_color:
            path_current = neighboor
            return 1



# Mandatory Pygame commands
pygame.init()
clock = pygame.time.Clock()

# You can change the image here:
maze = pygame.image.load('maze_hard.png')

# Make sure the maze is correctly diplayed by calculating the correct size.
mult = 1000 / maze.get_height()
win_size = (int(maze.get_width() * mult), int(maze.get_height() * mult))
surface = pygame.display.set_mode(win_size)
maze = maze.convert()

# Configuration of the colors used by the program.
red = (255,0,0,255)         # Color for the ending point
green = (0,255,0,255)       # Color for the starting point
white = (255,255,255,255)   # Color for the maze
black = (0,0,0,255)         # Color for the walls
yellow = (255,255,0,255)    # Color used to show the found path at the end

start = find_color(maze, green)
end = find_color(maze, red)

if start == Point(-1,-1) or end == Point(-1,-1):
    print('This image is not a valid maze. The starting point must be perfect green and the ending perfect red.')
    exit
    
state = 0           # State is used to define at what state of the program we are.
points = [start]    # Points is the list of points to expand from.
done = False
base_fps = 60
unlocked_fps = True;


result_lenght = 0

while not done:

    # State 0 means expanding, basically looking for the ending and marking
    # with different colors all the "maze" pixel in between.
    if state == 0:
        fps = base_fps
        state = expand()
        if points == []:
            print('No solution can be found. Please try another maze. Goodbye.')
            fps = 2
            state = 3

    # State 0 refers to tracing the path. The program start from the ending
    # and goes back to the start by looking for the previous color in the series.
    # Look at next_color and previous_color for more information on the series.
    elif state == 1:
        fps = base_fps * 5
        state = path()

    # At state 3, the program has finish its job. Decreases the fps and
    # display the lenght of the path
    elif state == 2:
        state = 3
        fps = 2
        print('Lenght of the path is ' + str(result_lenght) + '.')

    # Displays the maze and ticks pygame's clock
    surface.blit(pygame.transform.scale(maze, win_size), ((0, 0)))
    if not unlocked_fps: clock.tick(fps)
    pygame.display.flip()

    # Quit game if cross button clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# Close the window and quit
pygame.quit()
