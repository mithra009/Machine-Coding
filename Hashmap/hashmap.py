class Node:
    """Node used by the doubly linked list."""
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly linked list used for collision chaining."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_end(self, node):
        """Insert a node at the end of the list."""
        
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

        self.size += 1

    def remove_node(self, node):
        """Remove a given node from the list."""

        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None
        self.size -= 1


class HashMap:
    """
    HashMap implementation using separate chaining
    with doubly linked lists.
    """

    DEFAULT_CAPACITY = 5
    LOAD_FACTOR_THRESHOLD = 0.75
    RESIZE_FACTOR = 2

    def __init__(
        self,
        capacity=DEFAULT_CAPACITY,
        load_factor=LOAD_FACTOR_THRESHOLD
    ):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        if not 0 < load_factor < 1:
            raise ValueError("Load factor must be between 0 and 1")

        self.capacity = capacity
        self.count = 0
        self.load_factor = load_factor

        self.buckets = [
            DoublyLinkedList()
            for _ in range(self.capacity)
        ]

    def _hash(self, key):
        """
        Convert a key into a valid bucket index.

        Python's hash() requires the key to be hashable.
        """
        return hash(key) % self.capacity

    def _insert_node(self, node):
        """
        Insert an already-created node without checking
        load factor.

        Used during rehashing.
        """
        index = self._hash(node.key)
        self.buckets[index].insert_at_end(node)
        self.count += 1

    def _rehash(self):
        """Double capacity and redistribute all existing nodes."""

        old_buckets = self.buckets

        self.capacity *= self.RESIZE_FACTOR

        self.buckets = [
            DoublyLinkedList()
            for _ in range(self.capacity)
        ]

        old_count = self.count
        self.count = 0

        for bucket in old_buckets:
            current = bucket.head

            while current is not None:
                next_node = current.next

                current.prev = None
                current.next = None

                self._insert_node(current)

                current = next_node

        assert self.count == old_count

    def set(self, key, value):
        """
        Insert a new key-value pair.

        If key already exists, update its value.
        """

        index = self._hash(key)
        bucket = self.buckets[index]

        current = bucket.head

        while current is not None:
            if current.key == key:
                current.value = value
                return

            current = current.next

        node = Node(key, value)

        bucket.insert_at_end(node)
        self.count += 1

        if self.count / self.capacity > self.load_factor:
            self._rehash()

    def get(self, key, default=None):
        """Return value associated with key."""

        index = self._hash(key)
        bucket = self.buckets[index]

        current = bucket.head

        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        return default

    def contains(self, key):
        """Return True if key exists, otherwise False."""

        index = self._hash(key)
        bucket = self.buckets[index]

        current = bucket.head

        while current is not None:
            if current.key == key:
                return True

            current = current.next

        return False

    def remove(self, key):
        """
        Remove key from the hashmap.

        Returns:
            Removed value if key exists.
            None otherwise.
        """

        index = self._hash(key)
        bucket = self.buckets[index]

        current = bucket.head

        while current is not None:
            if current.key == key:
                value = current.value

                bucket.remove_node(current)
                self.count -= 1

                return value

            current = current.next

        return None

    def __len__(self):
        return self.count

    def display(self):
        """Display all buckets and their chains."""

        print(
            f"Capacity: {self.capacity}, "
            f"Size: {self.count}, "
            f"Load Factor: {self.count / self.capacity:.2f}"
        )

        for index, bucket in enumerate(self.buckets):

            print(f"Index {index}: ", end="")

            current = bucket.head

            if current is None:
                print("None")
                continue

            while current is not None:
                print(
                    f"({current.key}: {current.value})",
                    end=""
                )

                if current.next is not None:
                    print(" -> ", end="")

                current = current.next

            print()

    def clear(self):
        """Remove all entries while keeping current capacity."""

        self.buckets = [
            DoublyLinkedList()
            for _ in range(self.capacity)
        ]

        self.count = 0

if __name__ == "__main__":

    hashmap = HashMap()

    hashmap.set("key1", "value1")
    hashmap.set("key2", "value2")
    hashmap.set("key3", "value3")

    print("------------ Initial HashMap ------------")
    hashmap.display()

    print("\nGet key1:", hashmap.get("key1"))
    print("Get key2:", hashmap.get("key2"))
    print("Get missing:", hashmap.get("missing"))

    print("\nContains key1:", hashmap.contains("key1"))
    print("Contains key10:", hashmap.contains("key10"))

    hashmap.set("key1", "new_value1")

    print("\n------------ After Updating key1 ------------")
    hashmap.display()

    print("\nGet key1:", hashmap.get("key1"))

    removed = hashmap.remove("key2")

    print("\nRemoved:", removed)

    print("\n------------ After Removing key2 ------------")
    hashmap.display()

    for i in range(4, 15):
        hashmap.set(f"key{i}", f"value{i}")

    print("\n------------ After Adding More Keys ------------")
    hashmap.display()

    print("\nNumber of elements:", len(hashmap))

    hashmap.clear()

    print("\n------------ After Clear ------------")
    hashmap.display()