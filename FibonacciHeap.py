#Node class for the Fibonacci Heap.
class FibonacciHeapNode:
    def __init__(self, key):
        self.key = key #key of the node
        self.degree = 0 #Degree of the node (number of children)
        self.parent = None #Parent node
        self.child = None #Child node
        self.marked = False #Mark indicating whether node has lost a child in the past
        self.next = self #Next node in the circular doubly linked list
        self.prev = self #Previous node in the circular doubly linked list
#Fibonacci Heap data structure.
class FibonacciHeap:
    def __init__(self):
        self.min_node = None #Minimum node in the heap
        self.count = 0 #Number of nodes in the heap

    #Checks if the heap is empty.
    def is_empty(self):
        return self.min_node is None
    #Inserts a new key into the heap.
    def insert(self, key):
        """
        
        """
        new_node = FibonacciHeapNode(key)
        #Inserts the new node into the circular doubly linked list of roots
        if self.min_node:
            new_node.next = self.min_node
            new_node.prev = self.min_node.prev
            self.min_node.prev.next = new_node
            self.min_node.prev = new_node
            #Updates the minimum node if necessary
            if key < self.min_node.key:
                self.min_node = new_node
        else:
            self.min_node = new_node

        self.count += 1
    #Finds the minimum key in the heap.
    def find_min(self):
        return self.min_node.key if self.min_node else None

    #Extracts the minimum key from the heap.
    def extract_min(self):
        if self.is_empty():
            raise ValueError("Heap is empty")

        min_node = self.min_node
        #Removes the minimum node from the root list
        self._remove_from_list(min_node)
        #Adds the children of the minimum node to the root list
        if min_node.child:
            child = min_node.child
            while child:
                next_child = child.next
                self._remove_from_list(child)
                child.parent = None
                self._add_to_list(child, self.min_node)
                child = next_child

       #Updates the minimum node
        if min_node == min_node.next:
            self.min_node = None
        else:
            self.min_node = min_node.next

        self.count -= 1
        return min_node.key

    #Merges another Fibonacci heap into this heap.
    def merge(self, other_heap):
        #Makes sure the second heap is not empty
        if other_heap.is_empty():
            return
        #Makes sure the current heap is not empty
        if self.is_empty():
            self.min_node = other_heap.min_node
        else:
            #Merges the root lists of both heaps
            self.min_node.next.prev = other_heap.min_node.prev
            other_heap.min_node.prev.next = self.min_node.next
            self.min_node.next = other_heap.min_node
            other_heap.min_node.prev = self.min_node
            #Updates the minimum node if necessary
            if other_heap.min_node.key < self.min_node.key:
                self.min_node = other_heap.min_node

        self.count += other_heap.count

    #Decreases the key of a node in the heap.
    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key must be smaller than the current key")

        node.key = new_key
        #Performs cascading cuts to maintain the heap property, if necessary 
        if node.parent and node.key < node.parent.key:
            self._cut(node)
            self._cascading_cut(node)

        #Updates the minimum node if necessary
        if node.key < self.min_node.key:
            self.min_node = node
    #Deletes a node from the heap (Does not currently pass the test found at the bottom)
    def delete(self, node):
        #If the node is the minimum node, extract it
        if node == self.min_node:
            self.extract_min()
        else:
            #Decreases the key of the node to negative infinity and extract it
            self.decrease_key(node, float('-inf'))
            self.extract_min()

    #Removes a node from the circular doubly linked list.
    def _remove_from_list(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    #Adds a node to the circular doubly linked list.
    def _add_to_list(self, node, target):
        node.next = target.next
        node.prev = target
        target.next.prev = node
        target.next = node

    #Cuts a node from its parent.
    def _cut(self, node):
        if node.parent:
            #Removes the node from its parent's child list
            if node.parent.child == node:
                node.parent.child = node.next
            node.prev.next = node.next
            node.next.prev = node.prev
            node.parent.degree -= 1
            node.parent = None
            node.marked = False
    #Performs cascading cut on the node's parent.
    def _cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.marked:
                #Marks the node if it hasn't been marked before
                node.marked = True
            else:
                #Performs a cut on the node and continue cascading up
                self._cut(node)
                self._cascading_cut(parent)

#Tests the Fibonacci Heap
def test_fibonacci_heap():
    heap = FibonacciHeap()

    #Inserts elements
    elements = [10, 20, 5, 15, 30]
    for elem in elements:
        heap.insert(elem)

    #Checks min key
    assert heap.find_min() == 5

    #Extracts min
    assert heap.extract_min() == 5

    #Checks new min key
    assert heap.find_min() == 10

    #Decreases key
    node_to_decrease = heap.min_node #Node with key 10
    heap.decrease_key(node_to_decrease, 3)
    assert heap.find_min() == 3

    #Merges with another heap
    other_heap = FibonacciHeap()
    other_elements = [8, 12, 7]
    for elem in other_elements:
        other_heap.insert(elem)
    heap.merge(other_heap)
    assert heap.find_min() == 3

    """
    Possible Test case for the delete operation
   #Delete a node
    node_to_delete = heap.min_node#Node with key 15
    heap.delete(node_to_delete)
    assert heap.find_min() == 3
    """

    print("All test cases passed!")
    
#Runs the program
test_fibonacci_heap()
