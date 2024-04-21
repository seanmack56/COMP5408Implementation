#Defining the node
class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None  
        self.children = [] #List to store child nodes
        self.degree = 0 #Degree of the node (number of children)
        self.marked = False #Flag to indicate if the node has been marked

#Implementation of Binomial Heap data structure and operations
class BinomialHeap:
    def __init__(self):
        self.trees = [] #List of Binomial Trees
        self.min_node = None #Reference to the node with the minimum key in the heap
        self.count = 0 #Number of nodes in the heap

    def is_empty(self):
        return self.min_node is None
    #Inserts a new key into the heap
    def insert(self, key):
        node = Node(key) #Create a new node with the given key
        heap = BinomialHeap() #Create a new heap
        heap.trees.append(node) #Add the new node as a tree in the new heap
        self.merge(heap) #Merge the new heap with the current heap

    #Gets the minimum key value
    def get_min(self):
        return self.min_node.key if self.min_node else None
    
    #Extracts the nope with the minimum key value.
    def extract_min(self):
        if self.is_empty():
            raise ValueError("Heap is empty")

        min_node = self.min_node #Store the reference to the node with the minimum key
        self.trees.remove(min_node) #Remove the tree containing the minimum node from the heap
        heap = BinomialHeap() #Create a new heap
        heap.trees = min_node.children #Move the children of the minimum node to the new heap
        self.merge(heap) #Merge the new heap with the current heap
        self.find_min() #Find the new minimum node in the heap
        self.count -= 1 #Decrement the count of nodes
        return min_node.key #Return the key of the extracted minimum node
    
    #Performs merge between two heaps
    def merge(self, other_heap):
        self.trees.extend(other_heap.trees)  #Concatenate the lists of trees
        self.find_min() #Find the new minimum node in the merged heap

    #Decreases the key of a specific node. Often integral in performing delete.   
    def decrease_key(self, node, new_value):
        #Check if the new key value is greater thabn than the current node key
        if new_value > node.key:
            raise ValueError("New key must be smaller than the current key")

        node.key= new_value #Update node key value with new node key
        #While the node key value is less thsan its parent's
        while node.parent and node.key < node.parent.key:
            node.key, node.parent.key = node.parent.key, node.key #Swap the keys of the node and its parent.
            node = node.parent #Move to the parent of the current node

    #Finds the new minimum key value
    def find_min(self):
        if self.trees:
            self.min_node = min(self.trees, key=lambda x: x.key) #Find the node with the minimum key
        else:
            self.min_node = None #If there are no trees, set the minimum node to None

    """ Potential example of a Delete function    
    def delete(self, node):
       #Decrease the key of the node to negative infinity
        self.decrease_key(node, float('-inf'))
       #Extract the minimum (which is the node with negative infinity key)
        self.extract_min()
    """
# Test the Binomial Heap
def test_decrease_key():
    heap = BinomialHeap()

   #Insert elements
    elements = [10, 20, 5, 15, 30]
    for elem in elements:
        heap.insert(elem)

   #Check min key value
    assert heap.get_min() == 5

   #Decrease key
    node_to_decrease = heap.trees[2] #Node with key value 15
    heap.decrease_key(node_to_decrease, 3)
    assert heap.get_min() == 3

    #Extracts min
    extracted_min = heap.extract_min()
    assert extracted_min == 3
    assert heap.get_min() == 10

    #Inserts more elements
    heap.insert(8)
    heap.insert(3)

    #Checks min key value
    assert heap.get_min() == 3

    print("All tests passed successfully!")

#Runs the program
test_decrease_key()

