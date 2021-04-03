import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

global red1,red2,red3,blue1,blue2,blue3,blue4
global red1x,red1y,red2x,red3x,blue1x,blue2x,blue3x,blue4x,red2y,red3y,blue1y,blue2y,blue3y,blue4y,goalx,goaly

class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))
# A* search
def astar_search(graph, heuristics, start, end):
    
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name )
                current_node = current_node.parent
            path.append(start_node.name)
            # Return reversed path
            return path[::-1]
        # Get neighbours
        neighbors = graph.get(current_node.name)
        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            # Calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None
# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

"""

"""

def draw_line(surface,a,b):
    x1=0
    x2=0
    y1=0
    y2=0
    if a=="Blue1":
        x1=blue1x
        y1=blue1y
    elif a=="Blue2":
        x1=blue2x
        y1=blue2y
    elif a=="Blue3":
        x1=blue3x
        y1=blue3y        
    elif a=="Kicker(Blue4)":
        x1=blue4x
        y1=blue4y
    elif a=="Goal":
        x1=goalx
        y1=goaly        

    if b=="Blue1":
        x2=blue1x
        y2=blue1y
    elif b=="Blue2":
        x2=blue2x
        y2=blue2y
    elif b=="Blue3":
        x2=blue3x
        y2=blue3y        
    elif b=="Kicker(Blue4)":
        x2=blue4x
        y2=blue4y
    elif b=="Goal":
        x2=goalx
        y2=goaly   

    pygame.draw.line(surface, (0,0,0), (x1+15,y1),(x2+20,y2+5),2)           


def draw_lines(screen,path):

    global red1,red2,red3,blue1,blue2,blue3,blue4
    global red1x,red1y,red2x,red3x,blue1x,blue2x,blue3x,blue4x,red2y,red3y,blue1y,blue2y,blue3y,blue4y,goalx,goaly
    i = 0 
    for i in range(len(path)-1):
        j=i+1
        draw_line(screen,path[i],path[j])
        






def render_players(screen):


    global red1,red2,red3,blue1,blue2,blue3,blue4,football
    global red1x,red1y,red2x,red3x,blue1x,blue2x,blue3x,blue4x,red2y,red3y,blue1y,blue2y,blue3y,blue4y,goalx,goaly

    string=""
    font = pygame.font.Font('freesansbold.ttf', 12)
    score = font.render( string, True, (0 , 0, 0))
    screen.blit(score, (100, 550))

    x=0
    y=0
    #red1 x,y
    x=random.randrange(100, 440, 5)
    y=random.randrange(50, 140, 5)
    red1x=x
    red1y=y
    score = font.render("RED1", True, (0 , 0, 0))
    screen.blit(red1, (x, y))
    screen.blit(score, (x, y+15))

    #red2 x,y
    y=random.randrange(50, 340, 5)
    if y < 175:
        if random.randrange(1,10,1)%2 == 0 :
            x=random.randrange(490, 520, 5)
        else:
            x=random.randrange(40, 70, 5)  
    else:
         x=random.randrange(40, 520, 5)

    red2x=x
    red2y=y 
    score = font.render( "RED2", True, (0 , 0, 0))
    screen.blit(red2, (x, y))
    screen.blit(score, (x, y+15))

    #red3 x,y
    y=random.randrange(50, 340, 5)
    if y < 175:
        if random.randrange(1,10,1)%2 == 0 :
            x=random.randrange(490, 520, 5)
        else:
            x=random.randrange(40, 70, 5)  
    else:
         x=random.randrange(40, 520, 5)     

    red3x=x
    red3y=y     

    score = font.render("RED3", True, (0 , 0, 0))
    screen.blit(red3, (x, y))
    screen.blit(score, (x, y+15))

    #blue1 x,y
    x=random.randrange(100, 440, 5)
    y=random.randrange(50, 145, 5)

    blue1x=x
    blue1y=y
    score = font.render("BLUE1", True, (0 , 0, 0))
    screen.blit(blue1, (x, y))
    screen.blit(score, (x, y+15))
    



    #blue2 x,y
    y=random.randrange(50, 340, 5)
    if y < 175:
        if random.randrange(1,10,1)%2 == 0 :
            x=random.randrange(490, 520, 5)
        else:
            x=random.randrange(40, 70, 5)  
    else:
         x=random.randrange(40, 520, 5) 

    blue2x=x
    blue2y=y

    score = font.render("BLUE2", True, (0 , 0, 0))
    screen.blit(blue2, (x, y))
    screen.blit(score, (x, y+15))

    #blue3 x,y
    y=random.randrange(50, 340, 5)
    if y < 175:
        if random.randrange(1,10,1)%2 == 0 :
            x=random.randrange(490, 520, 5)
        else:
            x=random.randrange(40, 70, 5)  
    else:
         x=random.randrange(40, 520, 5)   

    blue3x=x
    blue3y=y  
    score = font.render("BLUE3", True, (0 , 0, 0))
    screen.blit(blue3, (x, y))
    screen.blit(score, (x, y+15))   

    #blue4 x,y
    x=random.randrange(40, 520, 5)
    y=random.randrange(50, 340, 5)
    x=272
    y=372
    blue4x=x
    blue4y=y
    score = font.render("KICKER(BLUE4)", True, (0 , 0, 0))
    screen.blit(blue4, (x, y))
    screen.blit(score, (x, y+15))
    screen.blit(football,(x,y-20))



def euclid_distance(x1,y1,x2,y2):
    distance=abs(x1-x2)+abs(y2-y1)
    return distance



def sqrt_distance(x1,y1,x2,y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + (math.pow(y1 - y2, 2)))
    return distance


def calculate(screen):

    global red1,red2,red3,blue1,blue2,blue3,blue4
    global red1x,red1y,red2x,red3x,blue1x,blue2x,blue3x,blue4x,red2y,red3y,blue1y,blue2y,blue3y,blue4y,goalx,goaly

    score_value=0
    graph = Graph()
    # Create graph connections (Actual distance)


    graph.connect('Kicker(Blue4)', 'Blue2', sqrt_distance(blue4x,blue4y,blue2x,blue2y))
    graph.connect('Kicker(Blue4)', 'Blue3', sqrt_distance(blue4x,blue4y,blue3x,blue3y))
    graph.connect('Kicker(Blue4)', 'Blue1', sqrt_distance(blue4x,blue4y,blue1x,blue1y))

    graph.connect( 'Goal','Blue2', sqrt_distance(goalx,goaly,blue2x,blue2y))
    graph.connect('Goal', 'Blue3', sqrt_distance(goalx,goaly,blue3x,blue3y))
    graph.connect('Goal', 'Blue1', sqrt_distance(goalx,goaly,blue1x,blue1y))

    graph.connect( 'Blue1','Blue2', sqrt_distance(blue1x,blue1y,blue2x,blue2y))
    graph.connect('Blue2', 'Blue3', sqrt_distance(blue2x,blue2y,blue3x,blue3y))
    graph.connect('Blue3', 'Blue1', sqrt_distance(blue3x,blue3y,blue1x,blue1y))    
    

    # Make graph undirected, create symmetric connections
    graph.make_undirected()
    # Create heuristics (straight-line distance, air-travel distance)
    heuristics = {}
    heuristics['Kicker(Blue4)'] = euclid_distance(blue4x,blue4y,goalx,goaly)
    heuristics['Blue1'] = euclid_distance(blue1x,blue1y,goalx,goaly)
    heuristics['Blue2'] = euclid_distance(blue2x,blue2y,goalx,goaly)
    heuristics['Blue3'] = euclid_distance(blue3x,blue3y,goalx,goaly)
    heuristics['Goal'] = 0

    # Run the search algorithm
    path = astar_search(graph, heuristics, 'Kicker(Blue4)', 'Goal')

#    print(path)

    string = "Path"

    for x in path:
        string = string + " -> -> " + x 

    print(string)    

   # print("calculating")
    #calculate score
    font = pygame.font.Font('freesansbold.ttf', 18)
    score = font.render( string, True, (0 , 0, 0))
    screen.blit(score, (100, 550))

    return path
    


def main():
    #setting up the screen
    screen = pygame.display.set_mode((570, 724))
    background = pygame.image.load('background.png')
    pygame.display.set_caption("Assignment")

    #globaling the player variables
    global red1,red2,red3,blue1,blue2,blue3,blue4,football
    global red1x,red1y,red2x,red3x,blue1x,blue2x,blue3x,blue4x,red2y,red3y,blue1y,blue2y,blue3y,blue4y,goalx,goaly

    goalx=290
    goaly=30
    #setting the game loop
    flag=True

    football=pygame.image.load('football.png')
    #Setting up the players --
    
    red1 = pygame.image.load('red.png')
    red2 = pygame.image.load('red.png')
    red3 = pygame.image.load('red.png')
    blue1 = pygame.image.load('blue.png')
    blue2 = pygame.image.load('blue.png')
    blue3 = pygame.image.load('blue.png')
    blue4 = pygame.image.load('blue.png')

    # creating a clock object

    clock = pygame.time.Clock() 


    #running the game loop

    while flag:

        pygame.time.delay(2500)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS


        screen.fill((0, 0, 0))
        # Background Image -- 
        screen.blit(background, (0, 0))
        

        #rendering the players ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

        render_players(screen)
        pygame.display.update()

        pygame.time.delay(3000)




        path=calculate(screen)
        draw_lines(screen,path)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        pygame.display.update()







main()