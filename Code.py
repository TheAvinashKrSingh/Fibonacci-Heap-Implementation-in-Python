class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.is_marked = False
        self.next = self
        self.prev = self

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    def insert(self, key):
        new_node = Node(key)
        if not self.min_node:
            self.min_node = new_node
        else:
            self._link(self.min_node, new_node)
            if key < self.min_node.key:
                self.min_node = new_node
        self.num_nodes += 1

    def _link(self, a, b):
        a_next = a.next
        a.next = b
        b.prev = a
        b.next = a_next
        a_next.prev = b

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

    def extract_min(self):
        if not self.min_node:
            return None
        min_node = self.min_node

        # If min_node has children, add them to the root list
        if min_node.child:
            child = min_node.child
            while True:
                next_child = child.next
                child.prev = self.min_node.prev
                child.next = self.min_node
                self.min_node.prev.next = child
                self.min_node.prev = child

                child.parent = None
                child = next_child
                if child == min_node.child:
                    break

        # Remove min_node from root list
        if min_node.next == min_node:  # Only one node
            self.min_node = None
        else:
            if min_node == self.min_node:
                self.min_node = min_node.next
            min_node.prev.next = min_node.next
            min_node.next.prev = min_node.prev

        self.num_nodes -= 1
        if self.min_node:
            self._consolidate()

        return min_node.key

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

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key is greater than current key")
        node.key = new_key
        parent = node.parent
        if parent and new_key < parent.key:
            self._cut(node, parent)
        if new_key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        if node.next != node:
            node.prev.next = node.next
            node.next.prev = node.prev
        if parent.child == node:
            parent.child = node.next if node.next != node else None
        parent.degree -= 1
        node.parent = None
        node.prev = node.next = node
        self._link(self.min_node, node)

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()

    def get_min(self):
        return self.min_node.key if self.min_node else None

    def display(self):
        if not self.min_node:
            print("Heap is empty.")
            return
        print("Fibonacci Heap:")
        current = self.min_node
        nodes = []
        while True:
            nodes.append(current.key)
            current = current.next
            if current == self.min_node:
                break
        print(" -> ".join(map(str, nodes)))

# Example Usage
def main():
    fib_heap1 = FibonacciHeap()
    fib_heap1.insert(3)
    fib_heap1.insert(7)
    fib_heap1.insert(9)

    fib_heap2 = FibonacciHeap()
    fib_heap2.insert(5)
    fib_heap2.insert(12)

    fib_heap3 = FibonacciHeap()
    fib_heap3.insert(1)
    fib_heap3.insert(4)
    fib_heap3.insert(10)

    heaps = [fib_heap1, fib_heap2, fib_heap3]
    heap_names = ["Heap 1", "Heap 2", "Heap 3"]

    while True:
        print("\nAvailable Fibonacci Heaps:")
        for i, heap in enumerate(heaps):
            print(f"{heap_names[i]}: ", end="")
            heap.display()

        print("\nChoose an operation:")
        print("1. Extract Min")
        print("2. Find Min")
        print("3. Decrease Key")
        print("4. Delete Key")
        print("5. Union")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            heap_index = int(input("Choose a heap (0, 1, 2): "))
            min_val = heaps[heap_index].extract_min()
            print(f"Extracted Min from {heap_names[heap_index]}: {min_val if min_val is not None else 'Heap is empty.'}")
            print(f"Updated {heap_names[heap_index]}: ", end="")
            heaps[heap_index].display()

        elif choice == '2':
            heap_index = int(input("Choose a heap (0, 1, 2): "))
            min_val = heaps[heap_index].get_min()
            print(f"Minimum in {heap_names[heap_index]}: {min_val if min_val is not None else 'Heap is empty.'}")

        elif choice == '3':
            heap_index = int(input("Choose a heap (0, 1, 2): "))
            key_to_decrease = int(input("Enter key to decrease: "))
            new_key = int(input("Enter new key: "))
            current = heaps[heap_index].min_node
            while current:
                if current.key == key_to_decrease:
                    heaps[heap_index].decrease_key(current, new_key)
                    print(f"Decreased key {key_to_decrease} to {new_key} in {heap_names[heap_index]}.")
                    break
                current = current.next
                if current == heaps[heap_index].min_node:
                    print("Key not found.")
                    break

        elif choice == '4':
            heap_index = int(input("Choose a heap (0, 1, 2): "))
            key_to_delete = int(input("Enter key to delete: "))
            current = heaps[heap_index].min_node
            while current:
                if current.key == key_to_delete:
                    heaps[heap_index].delete(current)
                    print(f"Deleted key {key_to_delete} from {heap_names[heap_index]}.")
                    break
                current = current.next
                if current == heaps[heap_index].min_node:
                    print("Key not found.")
                    break

        elif choice == '5':
            heap_index1 = int(input("Choose first heap (0, 1, 2): "))
            heap_index2 = int(input("Choose second heap (0, 1, 2): "))
            union_heap = heaps[heap_index1].union(heaps[heap_index2])
            print(f"Union of {heap_names[heap_index1]} and {heap_names[heap_index2]}: ", end="")
            union_heap.display()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
      
