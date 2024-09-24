# Fibonacci-Heap-Implementation-in-Python

Fibonacci Heap in Python

Overview

This repository contains a Python implementation of the Fibonacci Heap data structure. A Fibonacci Heap is a type of priority queue that supports operations like insertion, find minimum, extract minimum, union, decrease key, and delete key efficiently. It is particularly useful for graph algorithms like Dijkstra's and Prim's due to its amortized time complexity.

Features

- Insert: O(1) amortized time.

- Extract Min: O(log n) amortized time.

- Union: O(1) amortized time.

- Decrease Key: O(1) amortized time.

- Delete: O(log n) amortized time.

- Find Min: O(1) time.

Data Structure Overview

Node Class

Each node in the Fibonacci Heap is represented by the `Node` class, which contains:

- key: The value stored in the node.

- degree: Number of children.

- parent and child: Pointers to the parent and one of its children.

- next and prev: Pointers to the next and previous nodes in the circular doubly linked list.

- is_marked: Marks if the node has lost a child since it became a child of another node.

FibonacciHeap Class

The `FibonacciHeap` class manages the nodes and provides methods to manipulate the heap. It has:

- min_node: Pointer to the node with the smallest key.

- num_nodes: The number of nodes in the heap.

Algorithms

1. Insert Operation

Inserts a new node into the Fibonacci Heap.

Algorithm:

1. Create a new node with the given key.

2. Insert the node into the root list.

3. Update the `min_node` if the new node has a smaller key.

4. Increment the total number of nodes.

Code:



def insert(self, key):

    new_node = Node(key)

    if not self.min_node:

        self.min_node = new_node

    else:

        self._link(self.min_node, new_node)

        if key < self.min_node.key:

            self.min_node = new_node

    self.num_nodes += 1



2. Extract Min Operation

Removes and returns the node with the minimum key.

Algorithm:

1. If the `min_node` is `None`, return `None` (the heap is empty).

2. If the `min_node` has children, add each child to the root list.

3. Remove the `min_node` from the root list.

4. If the heap is not empty, perform a **Consolidate** operation to reorganize the heap.

5. Return the key of the removed node.

Code:



def extract_min(self):

    if not self.min_node:

        return None

    min_node = self.min_node

    if min_node.child:

        child = min_node.child

        while True:

            next_child = child.next

            self._link(self.min_node, child)

            child.parent = None

            child = next_child

            if child == min_node.child:

                break

    if min_node.next == min_node:

        self.min_node = None

    else:

        self.min_node = min_node.next

        self._consolidate()

    self.num_nodes -= 1

    return min_node.key



3. Union Operation

Merges two Fibonacci Heaps.

Algorithm:

1. If one of the heaps is empty, return the other heap.

2. Concatenate the root lists of the two heaps.

3. Update the `min_node` to be the smaller of the two.

4. Combine the number of nodes from both heaps.

Code:



def union(self, other_heap):

    new_heap = FibonacciHeap()

    if not self.min_node:

        return other_heap

    if not other_heap.min_node:

        return self



    new_heap.min_node = self.min_node

    new_heap.num_nodes = self.num_nodes + other_heap.num_nodes

    self_last = self.min_node.prev

    other_last = other_heap.min_node.prev

    self_last.next = other_heap.min_node

    other_heap.min_node.prev = self_last

    other_last.next = self.min_node

    self.min_node.prev = other_last

    if other_heap.min_node.key < self.min_node.key:

        new_heap.min_node = other_heap.min_node

    return new_heap



4. Decrease Key Operation

Decreases the key value of a given node.

Algorithm:

1. Update the node's key to the new value.

2. If the new key is less than its parent's key, cut the node from its parent and move it to the root list.

3. If the node becomes the new minimum, update the `min_node`.

Code:



def decrease_key(self, node, new_key):

    if new_key > node.key:

        raise ValueError("New key is greater than current key")

    node.key = new_key

    parent = node.parent

    if parent and new_key < parent.key:

        self._cut(node, parent)

    if new_key < self.min_node.key:

        self.min_node = node



5. Delete Operation

Deletes a node by decreasing its key to negative infinity and then extracting it.

Algorithm:

1. Decrease the node's key to negative infinity (`float('-inf')`).

2. Call the **Extract Min** operation to remove the node from the heap.

Code:



def delete(self, node):

    self.decrease_key(node, float('-inf'))

    self.extract_min()



6. Consolidate Operation

Reorganizes the heap after an `Extract Min` operation.

Algorithm:

1. Create an empty array `trees` to keep track of trees by their degrees.

2. Traverse through the root list and merge trees of the same degree until no two trees of the same degree remain.

3. Rebuild the root list from the remaining trees and update the `min_node`.

Code:



def _consolidate(self):

    max_degree = self.num_nodes

    trees = [None] * (max_degree + 1)

    current = self.min_node

    nodes = []

    while True:

        nodes.append(current)

        current = current.next

        if current == self.min_node:

            break

    for node in nodes:

        degree = node.degree

        while trees[degree]:

            other = trees[degree]

            if node.key > other.key:

                node, other = other, node

            self._link(node, other)

            node.degree += 1

            trees[degree] = None

            degree += 1

        trees[degree] = node

    self.min_node = None

    for tree in trees:

        if tree:

            if not self.min_node:

                self.min_node = tree

            elif tree.key < self.min_node.key:

                self.min_node = tree





7. Find Minimum Operation

Finds and returns the minimum key from the Fibonacci Heap without removing it.



Algorithm:

Return the key of the min_node, which holds the minimum value in the heap.

Code:



def  find_min(self):

    if not self.min_node:

        return None

    return self.min_node.key



Contributions

Contributions are welcome! Feel free to submit issues or pull requests to enhance the project.

