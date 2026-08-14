""" A node in the doubly linked list """
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None 

""" A doubly linked list """
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def insert_at_end(self, node):
        if not self.tail:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None 


""" A hashmap implementation using a doubly linked list for collision resolution """
class HashMap:
    def __init__(self, size=5):
        self.size = size
        self.count = 0
        self.map = [DoublyLinkedList() for _ in range(size)]
        self.load_factor_threshold = 0.75

    def _hash(self, key):
        return hash(key) % self.size

    def rehash(self):
        old_map = self.map
        self.size *= 2
        self.map = [DoublyLinkedList() for _ in range(self.size)]
        self.count = 0

        for linked_list in old_map:
            current = linked_list.head
            while current:
                self.set(current.key, current.value)
                current = current.next

    def set(self, key, value):
        index = self._hash(key)
        linked_list = self.map[index]

        current = linked_list.head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        new_node = Node(key, value)
        linked_list.insert_at_end(new_node)
        self.count += 1

        if self.count > self.load_factor_threshold * self.size:
            self.rehash()

    def get(self, key):
        index = self._hash(key)
        linked_list = self.map[index]

        current = linked_list.head
        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None     

    def remove(self, key):
        index = self._hash(key)
        linked_list = self.map[index]

        current = linked_list.head
        while current:
            if current.key == key:
                linked_list.remove_node(current)
                return True  
            current = current.next

        return False  

    def display(self):
        for i, linked_list in enumerate(self.map):
            current = linked_list.head
            if current:
                print(f"Index {i}: ", end="")
                while current:
                    print(f"({current.key}: {current.value})", end=" -> ")
                    current = current.next
                print("None")
            else:
                print(f"Index {i}: None")

         

if __name__ == "__main__":
    hashmap = HashMap()

    hashmap.set("key1", "value1")
    hashmap.set("key2", "value2")
    hashmap.set("key3", "value3")
    print("------------Initial HashMap:-------------")
    hashmap.display()
    print(hashmap.get("key1"))  
    print(hashmap.get("key2"))  

    hashmap.set("key1", "new_value1")
    print("------------After updating key1:-------------")
    hashmap.display()
    print(hashmap.get("key1"))  

    hashmap.remove("key2")
    print("------------After removing key2:-------------")
    hashmap.display()
    print(hashmap.get("key2"))  

    for i in range(4, 10):
        hashmap.set(f"key{i}", f"value{i}")
    print("------------After adding more keys (rehashing may occur):-------------")
    hashmap.display()
