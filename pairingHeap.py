#Defines a node for the Pairing Heap
class PairingHeapNode:
    def __init__(self, key):
        self.key = key #Key value stored in the node
        self.children = [] #List of children nodes of the current node
        self.next_sibling = None #Reference to the next sibling node

#Defines the Pairing Heap data structure
class PairingHeap:
    def __init__(self, root=None):
        self.root = None #Root node of the heap

   #Finds the minimum key in the heap
    def find_min(self):
        if not self.root:
            raise ValueError("Heap is empty")
        return self.root.key

   #Melds two pairing heaps
    def meld(self, heap2):
        if not heap2.root:
            return self
        if not self.root:
            return heap2
        if self.root.key < heap2.root.key:
           #If the root of the current heap has a smaller key, attaches heap2 to its children
            self.root.children.append(heap2.root)
            heap2.root.next_sibling = self.root
            return self
        else:
           #If the root of heap2 has a smaller key, attaches the current heap to its children
            heap2.root.children.append(self.root)
            self.root.next_sibling = heap2.root
            return heap2

   #Inserts a new node with given key into the heap
    def insert(self, key):
        new_node = PairingHeapNode(key)
        if not self.root:
           #If the heap is empty, makes the new node the root
            self.root = new_node
        else:
           #Otherwise, melds the new node with the current heap
            self.root = self.meld(PairingHeap(new_node))
        return new_node

   #Decreases the key of a node
    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key must be smaller than the current key")
        node.key = new_key
        if node != self.root:
            if node.next_sibling:
               #Removes the node from its siblings list
                node.next_sibling.children.remove(node)
                node.next_sibling = None
           #Re-melds the heap with the updated node
            self.root = self.meld(PairingHeap(root=node))

   #Deletes the node with the minimum key
    def delete_min(self):
        if not self.root:
            raise ValueError("Heap is empty")
        min_node = self.root
        if self.root.children:
           #Re-melds the heap with its children to remove the minimum node
            self.root = self.meld(self, PairingHeap())
        else:
            self.root = None #If there are no children, sets the root to None
        return min_node.key

   #Deletes a specific node from the heap
    def delete(self, node):
        if node == self.root:
           #If the node is the root, calls delete_min
            self.delete_min()
        else:
            if node.next_sibling:
               #Removes the node from its siblings list
                node.next_sibling.children.remove(node)
                node.next_sibling = None
           #Re-meld the heap without the deleted node
            self.root = self.meld(self, PairingHeap())

#Tests the PairingHeap
def test_pairing_heap():
    heap = PairingHeap()
    #Checks insert
    node1 = heap.insert(10)
    node2 = heap.insert(20)
    node3 = heap.insert(5)
    
    #Checks min key value
    assert heap.find_min() == 5

    #Checks decrease_key
    heap.decrease_key(node2, 15)
    assert heap.find_min() == 5

    #Checks delete_min
    heap.delete_min()
    assert heap.find_min() == 10

    #checks delete
    heap.delete(node1)
    assert heap.find_min() == 15

    print("All tests passed!")

#Runs the test
test_pairing_heap()
