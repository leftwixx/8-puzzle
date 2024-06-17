import math

class Problem:
    vector = []
    algorithm = 0
    size = 0
    frontier = []
    priority = []
    explored = []
    allvectors = []
    path = [-1]
    depth = [0]
    currentposition = 0
    currentdepth = 0
    frontiermax = 0
    def __init__(self, v, a):
        self.vector = v
        self.algorithm = a
        self.size = get_size(v)
        self.frontier = [v]
        self.allvectors = [v]
        self.priority = [heuristic(v, 0, a)]


def graph_search(p):
    print_grid(p.vector)
    print()
    while(True):
        #if the node is the goal state, return true
        if(check(p.vector)):
            return True
        
        child1 = p.vector.copy()
        child2 = p.vector.copy()
        child3 = p.vector.copy()
        child4 = p.vector.copy()
        p.currentdepth = p.currentdepth + 1
        p.position = p.vector.index('*')
        if(p.position % p.size != 0):
            move_left(child1)
            updateAll(child1, p.allvectors, p.currentdepth, p.depth, p.currentposition, p.path, p.frontier, p.priority, p.algorithm)
        if(p.position % p.size != p.size - 1):
            move_right(child2)
            updateAll(child2, p.allvectors, p.currentdepth, p.depth, p.currentposition, p.path, p.frontier, p.priority, p.algorithm)
        if(p.position >= p.size):
            move_up(child3)
            updateAll(child3, p.allvectors, p.currentdepth, p.depth, p.currentposition, p.path, p.frontier, p.priority, p.algorithm)
        if(p.position < p.size * p.size - p.size):
            move_down(child4)
            updateAll(child4, p.allvectors, p.currentdepth, p.depth, p.currentposition, p.path, p.frontier, p.priority, p.algorithm)
        
        #updates the frontiermax
        if p.frontiermax < len(p.frontier):
            p.frontiermax = len(p.frontier)
        
        #pops the current node out of the frontier
        p.explored.append(p.vector)
        index = p.frontier.index(p.vector)
        p.frontier.pop(index)
        p.priority.pop(index)

        #if the frontier is empty, return false
        if(not p.frontier):
            return False
        

        #iterates to the next highest priority node in the frontier
        minval = p.priority.index(min(p.priority))
        p.vector = p.frontier[minval]
        p.currentposition = p.allvectors.index(p.vector)
        p.currentdepth = p.depth[p.currentposition]
        if p.algorithm == 1:
            print("The best state to expand with g(n) =", p.currentdepth, "is:")
        elif p.algorithm == 2:
            print("The best state to expand with g(n) =", p.currentdepth, "h(n) = ", misplaced(p.vector), "is:")
        elif p.algorithm == 3:
            print("The best state to expand with g(n) =", p.currentdepth, "h(n) = ", distance(p.vector), "is:")
        print_grid(p.vector)
        print()

#prints the path of the solution
def print_path(allvectors, path, position):
    if(path[position] == -1):
        print_grid(allvectors[0])
        print()
        return 0
    newposition = path[position]
    print_path(allvectors, path, newposition)
    print_grid(allvectors[position])
    print()

#prints the vector like the puzzle
def print_grid(vector):
    size = get_size(vector)
    for i in range(1, size + 1):
        for x in range((i - 1) * size, (i * size)):
            print(vector[x], end = " ")
        print() #newline

#returns the size
# for a 3x3 puzzle, the size is 3
def get_size(vector):
    full_size = len(vector)
    size = int(math.sqrt(full_size))
    return size
    

def move_left(vector):
    size = get_size(vector)
    position = vector.index('*')
    if(position % size != 0):
        temp = vector[position]
        vector[position] = vector[position - 1]
        vector[position - 1] = temp
    
def move_right(vector):
    size = get_size(vector)
    position = vector.index('*')
    if(position % size != size - 1):
        temp = vector[position]
        vector[position] = vector[position + 1]
        vector[position + 1] = temp

def move_up(vector):
    size = get_size(vector)
    position = vector.index('*')
    if(position >= size):
        temp = vector[position]
        vector[position] = vector[position - size]
        vector[position - size] = temp

def move_down(vector):
    size = get_size(vector)
    position = vector.index('*')
    if(position < size * size - size):
        temp = vector[position]
        vector[position] = vector[position + size]
        vector[position + size] = temp


#returns the euclidean distance
def distance(vector):
    size = get_size(vector)
    full_size = size * size
    sum = 0
    for i in range(0, full_size - 1):
        numberposition = vector.index(i + 1)
        rowdifference = abs(numberposition//size - i//size)
        columndifference = abs(numberposition%size - i%size)
        
        x = rowdifference * rowdifference
        y = columndifference * columndifference
        
        sum = sum + math.sqrt(x + y)
    return sum


#returns the amount of misplaced tiles
def misplaced(vector):
    size = get_size(vector)
    full_size = size * size
    sum = 0
    for i in range(0, full_size):
        if vector[i] != i + 1 and vector[i] != '*':
            sum = sum + 1
    return sum

#returns g(n) + h(n) for all algorithms
#for uniform cost, h(n) = 0
def heuristic(vector, depth, algorithm):
    if algorithm == 1:
        return depth
    elif algorithm == 2:
        return depth + misplaced(vector)
    else:
        return depth + distance(vector)

#check to see if the problem is solved
#True if its solved
#False if its not solved
def check(vector):
    size = get_size(vector)
    full_size = size * size
    for i in range(0, full_size):
        if vector[i] != i + 1 and vector[i] != '*':
            return False
    return True

#check to see if 2 vectors are the same.
#True if they are the same
#False if they are different
def vector_equality(vector1, vector2):
    if len(vector1) != len(vector2):
        return False
    else:
        length = len(vector1)
        for i in range(0, length):
            if vector1[i] != vector2[i]:
                return False
        return True

#adds the child node and all of the values needed to the multiple vectors
#it does not add the child node if the vector already exists in allvectors
def updateAll(child, allvectors, currentdepth, depth, currentposition, path, frontier, priority, algorithm):
    iterator = 0
    repeatedchild = False
    for x in allvectors:
        if (vector_equality(child, x)):
            repeatedchild = True
            if(heuristic(child, currentdepth, algorithm) < heuristic(x, depth[iterator], algorithm)):
                depth[iterator] = currentdepth
                path[iterator] = currentposition
        iterator = iterator + 1
    if(not repeatedchild):
        frontier.append(child)
        allvectors.append(child)
        path.append(currentposition)
        priority.append(heuristic(child, currentdepth, algorithm))
        depth.append(currentdepth)
    repeatedchild = False


#puzzle = vector of values
#size = size of puzzle, 3x3 = size 3
puzzle = []
invalid = True
while invalid:
    selection = int(input("Welcome to achan381(862272108) 8 puzzle solver.Type “1” to use a default puzzle, or “2” to enter your own puzzle "))
    print()
    if selection == 1:
        #default puzzle
        # 1 * 3
        # 4 2 6
        # 7 5 8
        size = 3
        square = size * size
        puzzle = [1, '*', 3, 4, 2, 6, 7, 5, 8]
        invalid = False
    elif selection == 2:
        print("Enter your puzzle, use 0 to represent the blank")
        puzzle = [0] * 9
        puzzle[0], puzzle[1], puzzle[2] = input("Enter 3 values, use space between numbers: ").split()
        puzzle[3], puzzle[4], puzzle[5] = input("Enter 3 values, use space between numbers: ").split()
        puzzle[6], puzzle[7], puzzle[8] = input("Enter 3 values, use space between numbers: ").split()
        invalid = False
        for i in range(0, len(puzzle)):
            puzzle[i] = int(puzzle[i])
        for i in range(0, len(puzzle)):
            if(i not in puzzle):
                print("Invalid: Missing ", i)
                invalid = True
            
        puzzle[puzzle.index(0)] = '*'
    else:
        print("invalid")
        invalid = True


invalid = True
while invalid:
    selection = int(input("Enter your choice of algorithm \n Uniform Cost Search (1) \n A* with Misplaced Tile Heuristic (2) \n A* with Euclidean Distance Heuristic (3) \n"))
    print()
    if selection == 1:
        print("Using Uniform Cost: \n")
        invalid = False
    elif selection == 2:
        print("Using Misplaced Tiles: \n")
        invalid = False
    elif selection == 3:
        print("Using Euclidean Distance: \n")
        invalid = False
    else:
        print("invalid\n")
        invalid = True

problem = Problem(puzzle, selection)
if(graph_search(problem)):
    print("==========GOAL==========")
    print_path(problem.allvectors, problem.path, problem.currentposition)
    print("To solve this problem the search algorithm expanded a total of", len(problem.explored), "nodes.")
    print("The maximum number of nodes in the queue at any one time:", problem.frontiermax)
    print("The depth of the goal was", problem.currentdepth)
else:
    print("==========No Solution==========")
    print("This problem expanded a total of", len(problem.explored), "nodes.")
    print("The maximum number of nodes in the queue at any one time:", problem.frontiermax)


#Test Cases
"""
testcase1 = [1, 2, 3, 4, 5, 6, 7, 8, '*'] #trivial
testcase2 = [1, 2, 3, 4, 5, 6, 7, '*', 8] #very easy
testcase3 = [1, 2, '*', 4, 5, 3, 7, 8, 6] #easy
testcase4 = ['*', 1, 2, 4, 5, 3, 7, 8, 6] #doable
testcase5 = [8, 7, 1, 6, '*', 2, 5, 4, 3] #oh boy
testcase6 = [1, 2, 3, 4, 5, 6, 8, 7, '*'] #impossible

problem2 = Problem(testcase5, 3)
if(graph_search(problem2)):
    print("==========GOAL==========")
    print_path(problem2.allvectors, problem2.path, problem2.currentposition)
    print("To solve this problem the search algorithm expanded a total of", len(problem2.explored), "nodes.")
    print("The maximum number of nodes in the queue at any one time:", problem2.frontiermax)
    print("The depth of the goal was", problem2.currentdepth)
else:
    print("==========No Solution==========")
    print("This problem expanded a total of", len(problem2.explored), "nodes.")
    print("The maximum number of nodes in the queue at any one time:", problem2.frontiermax)
"""