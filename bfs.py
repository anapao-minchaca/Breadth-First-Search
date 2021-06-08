'''
Created November 4, 2020

@Authors:
- Emilio Popovits Blake (A01027265)
- Patricio Tena (A01027293)
- Ana Paola Minchaca (A01026744)
- Rodrigo Benavente (A01026973)
'''

from os import listdir, path

class Node():
    def __init__(self, data):
        self.data = data
        self.neighbors = []

    
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
        

    def __eq__(self,other):
        if (isinstance(other, Node)):
            return self.data == other.data and self.neighbors == other.neighbors
        return False


def printObjectArray(array):
    tmpArray = []
    for element in array:
        tmpArray.append(element.data)
    
    return tmpArray


if __name__ == '__main__':
    # Prompt user to select file with NFA and read it
    print('Files in ./Graphs/ directory:')
    fileArray = []
    count = 1
    for file in listdir('./Graphs'):
            if file.endswith('.txt'):
                    print(path.join(str(count) + '. ', file))
                    fileArray.append(file)
                    count += 1
    
    prompt = input('\nWhich file number contains the undirected graph G that you want to run BFS on?: ')
    selectedFile = fileArray[int(prompt)-1]

    file = open('./Graphs/' + selectedFile)
    inputGraph = file.read()
    inputGraph = ''.join(inputGraph.split())

    print('\nRecieved undirected graph G string:')
    print(inputGraph)

    # Step 1: Parse input string and build nodeList array and edgeList array
    # inputGraph = '[[v1,v2,v3,v4,v5,v6,v7,v8,v9],[[v1,v2],[v1,v3],[v1,v4],[v2,v1],[v2,v3],[v2,v5],[v2,v6],[v3,v1],[v3,v2],[v3,v7],[v3,v8],[v4,v1],[v4,v8],[v5,v2],[v6,v2],[v7,v3],[v7,v9],[v8,v3],[v8,v4],[v9,v7]]]'
    inputGraph = inputGraph[1:len(inputGraph)-1]

    inputNodes = inputGraph.split('],[')[0]
    inputEdges = inputGraph.split(',[[')[1]
    inputEdges = inputEdges[0:len(inputEdges)-2].replace('],[',';').split(';')
    
    nodeList = inputNodes[1:len(inputNodes)].split(',')
    edgeList = []
    for tupple in inputEdges:
        tupple = tupple.split(',')
        edgeList.append(tupple)
    
    # Step 2: Build Node objects from nodeList and add them to nodeArray
    nodeArray = []
    for node in nodeList:
        newNode = Node(node)
        nodeArray.append(newNode)
    
    # Step 3: Loop through every tupple in edgeList and append neighbors to each node
    for index in range(len(edgeList)):
        edge = edgeList.pop(0)

        currentNode = [None,-1]
        neighborNode = None

        for index, node in enumerate(nodeArray):
            if node.data == edge[0]:
                currentNode[0] = node
                currentNode[1] = index
        
        for node in nodeArray:
            if node.data == edge[1]:
                neighborNode = node
        
        currentNode[0].addNeighbor(neighborNode)
        nodeArray[currentNode[1]] = currentNode[0]
    
    # Step 4: Set BFS algorithm initial conditions
    Q = [nodeArray[0]]
    A = [nodeArray[0]]
    L = []

    print('\nNode Graph (Table form):')
    print('Node\tNeighbors')
    print('---------------------------')
    for node in nodeArray:
        print(node.data + '\t', printObjectArray(node.neighbors))

    print('\nInitial Condition:')
    print('----------------------------')
    print('Queue Q:', printObjectArray(Q))
    print('Visited Array A:', printObjectArray(A))

    # Step 5: Follow BFS algorithm
    iterationCount = 0
    while len(Q) != 0:
        print('\nIteration ' + str(iterationCount + 1) + ':')
        print('----------------------------')
        
        nodeObj = Q.pop()
        L.append(nodeObj)
        neighbors = nodeObj.neighbors

        tmpA = A.copy()
        discardNodes = []

        # Build an array of nodes that must be appended to Q and A (neighbor nodes that are not in A)
        for node in tmpA:
            for neighbor in neighbors:
                if node == neighbor:
                    neighbors.remove(node)
                    discardNodes.append(node)
        
        # For each neighbor that's not in A, insert it to Q in the first position and append it to A
        for node in neighbors:
            Q.insert(0, node)
            A.append(node)

        print('Popped Node ' + nodeObj.data + ' From Q')
        print('Neighbors to add to Q and A: ', printObjectArray(neighbors))
        if len(discardNodes) != 0:
            print('Neighbors to discard from adding to Q and A: ', printObjectArray(discardNodes))
        print('Q:', printObjectArray(Q))
        print('A:', printObjectArray(A))
        
        iterationCount += 1
    
    print('\nFinished Iterating.')
    print('\nOrder L of traversing graph G by BFS:')
    print('----------------------------')
    print('L: ', printObjectArray(L))