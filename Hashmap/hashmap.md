# HashMap: Complete Guide

**Author:** Mithravardhan P N

---

## Table of Contents
1. [Introduction](#introduction)
2. [What is a HashMap?](#what-is-a-hashmap)
3. [Why Use HashMap?](#why-use-hashmap)
4. [Time & Space Complexity](#time--space-complexity)
5. [Why Array Alone is Not Optimal](#why-array-alone-is-not-optimal)
6. [Hash Function & Hash Code](#hash-function--hash-code)
7. [Collision Handling](#collision-handling)
8. [Why Doubly Linked List?](#why-doubly-linked-list)
9. [Load Factor](#load-factor)
10. [Rehashing](#rehashing)
11. [Designing a HashMap](#designing-a-hashmap)
12. [Best Practices](#best-practices)

---

## Introduction

A **HashMap** is one of the most fundamental and widely-used data structures in computer science. It implements an associative array—a structure that maps keys to values using a **hash function**. The main goal is to achieve O(1) average-case time complexity for search, insertion, and deletion operations.

---

## What is a HashMap?

A HashMap is a hash table-based implementation of a map that uses:
- **Keys**: Unique identifiers
- **Values**: Data associated with each key
- **Hash Function**: Converts keys into array indices

### Basic Structure
```
HashMap = [Array of Buckets/Slots]
Each Bucket can contain a Linked List of Key-Value pairs
```

**Example (Python):**
```python
# Create a HashMap
my_map = HashMap()

# Store key-value pair
my_map.put("apple", 5)

# Retrieve value
value = my_map.get("apple")  # Returns: 5
```

**Built-in Python dict:**
```python
my_map = {}
my_map["apple"] = 5      # Store
value = my_map["apple"]  # Retrieve: 5
```

---

## Why Use HashMap?

1. **Fast Lookups**: Average O(1) time complexity for get/put/remove operations
2. **Flexibility**: Works with any type of keys and values
3. **Memory Efficient**: Only stores what's needed (vs. arrays which need contiguous space)
4. **Dynamic Resizing**: Can grow as more elements are added
5. **Real-world Applications**:
   - Caching and memoization
   - Symbol tables in compilers
   - Frequency counting
   - Duplicate detection
   - Grouping data by keys

---

## Time & Space Complexity

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|--------------|-----------|
| **Get**   | O(1)         | O(n)      |
| **Put**   | O(1)         | O(n)      |
| **Remove**| O(1)         | O(n)      |
| **Contains** | O(1)      | O(n)      |

**Average Case**: When hash function distributes keys uniformly
**Worst Case**: When all keys hash to the same index (all collisions)

### Space Complexity

- **O(n)** where n is the number of key-value pairs stored

---

## Why Array Alone is Not Optimal

### Problems with Plain Array:

1. **Fixed Size**: Arrays have fixed capacity; can't grow dynamically
2. **Memory Waste**: Must allocate large arrays upfront; wasted space if data is sparse
3. **Index Limitations**: 
   - Array indices must be integers in range [0, size)
   - What if we want to use String keys? Or object keys?
   - Can't directly map arbitrary data types to indices
4. **No Direct Key Mapping**:
   - Array maps integer indices to values
   - We need a way to map arbitrary keys to indices
   - Solution: **Hash Function**

### Example Problem:
```
Array for Strings?
arr[0] = value for "apple"
arr[1] = value for "banana"

❌ How do we know "apple" maps to index 0?
❌ What if we have 1 million unique strings?
❌ Need to allocate array of size 1 million upfront
```

**Solution**: Hash function converts any key to an array index!

---

## Hash Function & Hash Code

### What is a Hash Function?

A hash function is a deterministic function that:
- **Input**: Any key (string, object, number, etc.)
- **Output**: An integer index in the range [0, capacity-1]
- **Deterministic**: Same input always produces same output
- **Fast**: Should compute quickly

### Hash Code Generation

```
hashCode(key) → Integer (can be negative/very large)
```

**Example:**
```
hashCode("apple") = 2015475421
hashCode("banana") = -1234567890
```

### Compression Function (Index Mapping)

Convert large hash code to valid array index:
```
index = Math.abs(hashCode) % capacity
```

**Example with capacity = 16:**
```
hashCode("apple") = 2015475421
index = 2015475421 % 16 = 13

hashCode("banana") = -1234567890
index = |-1234567890| % 16 = 2
```

### Why Hash Code?

1. **Uniform Distribution**: Good hash functions distribute keys uniformly
2. **Efficient**: Can compute in O(1) time
3. **Deterministic**: Reproducible results
4. **Any Data Type**: Works with strings, objects, numbers, etc.

### Properties of a Good Hash Function:

- **Deterministic**: hashCode(x) always returns same value
- **Efficient**: O(1) time to compute
- **Uniformly Distributed**: Keys spread evenly across array
- **Minimize Collisions**: Different keys should have different hashes
- **Avalanche Effect**: Small change in key → big change in hash

---

## Collision Handling

### What is a Collision?

When two different keys hash to the same index:
```
hashCode("apple") % 16 = 5
hashCode("apricot") % 16 = 5  ← COLLISION!
```

### Collision Resolution Techniques:

#### 1. **Separate Chaining** (Most Common)
Store colliding elements in a linked list at that index.

```
Index 5: "apple" → "apricot" → "avocado" → NULL
         (chain of colliding keys)
```

**Pros**: Simple, handles unlimited collisions
**Cons**: Extra memory for pointers

#### 2. **Open Addressing** (Linear/Quadratic Probing)
Find next empty slot in array.

```
Index 5: "apple"
Index 6: "apricot"  (moved here due to collision)
Index 7: "avocado"  (moved here due to collision)
```

**Pros**: Better cache locality
**Cons**: Requires empty slots; can cause clustering

#### 3. **Double Hashing**
Use second hash function to find next slot.

```
nextIndex = (hash1(key) + i * hash2(key)) % capacity
```

### Why Separate Chaining?

Separate chaining (using linked lists) is most commonly used because:
- Simple to implement
- Dynamic sizing within each bucket
- Good balance between performance and memory
- Easy to handle collisions

---

## Why Doubly Linked List?

In modern HashMap implementations, we often use **Doubly Linked Lists** instead of simple singly linked lists, especially for collision chains and LRU caching.

### Singly Linked List (Basic)
```
Node1 → Node2 → Node3 → NULL
prev field: NOT available
```

### Doubly Linked List (Better)
```
NULL ← Node1 ⇄ Node2 ⇄ Node3 ← NULL
       prev/next both available
```

### Advantages of Doubly Linked List:

1. **Efficient Removal**: Can remove element in O(1) if you have a reference
   ```
   Singly: Must traverse from head O(n)
   Doubly: Remove directly via prev pointer O(1)
   ```

2. **LRU Cache Implementation**: Easy to maintain insertion order
   - Move recently accessed items to end
   - Remove least recently used from front

3. **Bidirectional Traversal**: Can traverse forward and backward

4. **Collision Chain Navigation**: Better for handling chains efficiently

### Example (LRU Cache with Doubly Linked List):
```
Least Recently Used → ... → Most Recently Used
Access order maintained easily with prev/next pointers
```

### Trade-offs:
- **Pro**: Faster removal (O(1) vs O(n))
- **Pro**: Maintains insertion/access order easily
- **Con**: Extra memory for prev pointer
- **Con**: Slightly more complex implementation

---

## Load Factor

### Definition

**Load Factor (α)** = (Number of elements) / (Capacity of array)

```
α = n / capacity
```

### Significance

- **Low Load Factor (α < 0.5)**: Few collisions, fast operations, wasted space
- **High Load Factor (α > 0.75)**: Many collisions, slow operations, efficient space

### Example:
```
Capacity = 16
Elements = 12
Load Factor = 12 / 16 = 0.75
```

### Impact on Performance:

As load factor increases:
- **Collisions increase**: More keys hash to same index
- **Chain length increases**: Each chain gets longer
- **Operations slow down**: More comparisons needed

**Performance Graph:**
```
Time Complexity
      |     High α (many collisions)
      |    /
  O(n)|   /
      |  /
  O(1)|_/_______________
      |   Low α (few collisions)
      |________________ Load Factor →
```

### Load Factor Threshold

- **Java HashMap**: Uses α ≤ 0.75 (triggers rehash at 75% capacity)
- **Python dict**: Uses α ≤ 0.67 (triggers rehash at 2/3 capacity)
- **General recommendation**: 0.6 to 0.75

---

## Rehashing

### What is Rehashing?

Rehashing is the process of creating a new, larger hash table and reinserting all elements into it.

### Why Rehash?

As elements are added:
- Load factor increases
- Collisions become more frequent
- Operations become slower
- To maintain O(1) average-case performance

### When to Rehash?

**Typical Triggers:**
- When load factor exceeds threshold (usually 0.75)
- When number of elements > threshold value

### How Rehashing Works:

```
Step 1: Detect load factor exceeds threshold
        α = n / capacity > threshold (e.g., 0.75)

Step 2: Create new array with larger capacity
        new_capacity = capacity * 2  (usually double)

Step 3: Recompute hash codes for all elements
        new_index = hashCode(key) % new_capacity
        (indices change because capacity changed!)

Step 4: Reinsert all elements into new array
        for each (key, value) in old_map:
            new_map[hashCode(key) % new_capacity] = value

Step 5: Replace old array with new array
        map.array = new_array
```

### Visual Example:

**Before Rehashing:**
```
Capacity = 4
Elements = 3
Load Factor = 3/4 = 0.75 (reaches threshold)

Index 0: "a"
Index 1: "b" → "e"  (collision)
Index 2: (empty)
Index 3: "c" → "d"  (collision)
```

**After Rehashing (capacity doubled to 8):**
```
Recompute indices with new capacity:
"a": hashCode % 8 = 0  → Index 0
"b": hashCode % 8 = 1  → Index 1
"c": hashCode % 8 = 3  → Index 3
"d": hashCode % 8 = 5  → Index 5
"e": hashCode % 8 = 6  → Index 6

New array:
Index 0: "a"
Index 1: "b"
Index 2: (empty)
Index 3: "c"
Index 4: (empty)
Index 5: "d"
Index 6: "e"
Index 7: (empty)
```

**Benefits**: Fewer collisions, better distribution, faster lookups!

---

## Why Double the Size?

### Why Not Just Increase by 1?

**Example: Add 1000 elements, capacity grows by 1 each time**

```
Start: capacity = 10
Add 1st elem: capacity = 11, rehash 1 element
Add 2nd elem: capacity = 12, rehash 11 elements
Add 3rd elem: capacity = 13, rehash 12 elements
...
Add 1000th: capacity = 1010, rehash 1009 elements

Total rehashes: 1 + 11 + 12 + ... + 1009 = O(n²)
```

### Why Double the Size?

**Example: Doubling strategy with 1000 elements**

```
Start: capacity = 10
Add elements to 20: capacity doubles to 20, rehash 10 elements
Add elements to 40: capacity doubles to 40, rehash 20 elements
Add elements to 80: capacity doubles to 80, rehash 40 elements
Add elements to 160: capacity doubles to 160, rehash 80 elements
...

Total rehashes: 10 + 20 + 40 + 80 + ... ≈ 2 × 1000 = O(n)
```

### Analysis:

**Geometric Growth (Doubling):**
- Rehash count: $2^0 + 2^1 + 2^2 + ... + 2^k$ ≈ $2^{k+1}$
- Total operations: O(n) amortized

**Linear Growth (Add 1):**
- Rehash count: $1 + 2 + 3 + ... + n$ = $\frac{n(n+1)}{2}$ = O(n²)
- Total operations: O(n²) amortized

### Why Not Triple or Double-Plus-One?

**Why specifically 2x?**
- 2x is optimal balance between:
  - Memory efficiency (not too much waste)
  - Time efficiency (not too many rehashes)
  - Simple binary operation (multiply by 2 = bit shift)

**Other strategies:**
- 1.5x: Also common, slightly more memory efficient
- 3x: Too wasteful of memory
- Variable: Some implementations use different factors

---

## Designing a HashMap

### Key Components:

1. **Hash Function** → Convert key to hash code
2. **Compression Function** → Map hash code to index [0, capacity)
3. **Collision Resolution** → Handle collisions (separate chaining)
4. **Resizing Logic** → Rehash when load factor exceeded
5. **Entry Storage** → Store key-value pairs

### Implementation Overview (Python):

```python
class Entry:
    """Node for linked list in separate chaining"""
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMap:
    """
    Custom HashMap implementation using separate chaining
    for collision resolution
    """
    
    def __init__(self, capacity=10):
        """
        Initialize HashMap
        Args:
            capacity: Initial capacity of the hash table (default: 10)
        """
        self.capacity = capacity
        self.table = [None] * capacity  # Array of buckets (linked lists)
        self.size = 0                    # Number of entries
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """
        Hash function: convert key to array index
        Args:
            key: Key to hash
        Returns:
            Index in range [0, capacity)
        """
        if key is None:
            return 0
        return abs(hash(key)) % self.capacity
    
    def put(self, key, value):
        """
        Insert or update a key-value pair
        Args:
            key: Key to insert
            value: Value associated with key
        """
        # Check if rehashing needed
        if self.size / self.capacity >= self.load_factor_threshold:
            self._rehash()
        
        # Compute index
        index = self._hash(key)
        
        # Traverse linked list at this index
        entry = self.table[index]
        while entry is not None:
            if entry.key == key:
                # Update existing key
                entry.value = value
                return
            entry = entry.next
        
        # Insert new entry at head of linked list
        new_entry = Entry(key, value, self.table[index])
        self.table[index] = new_entry
        self.size += 1
    
    def get(self, key):
        """
        Retrieve value for a key
        Args:
            key: Key to search for
        Returns:
            Value if found, None otherwise
        """
        index = self._hash(key)
        
        # Traverse linked list at this index
        entry = self.table[index]
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        
        return None  # Key not found
    
    def remove(self, key):
        """
        Remove a key-value pair
        Args:
            key: Key to remove
        Returns:
            Value if found and removed, None otherwise
        """
        index = self._hash(key)
        
        entry = self.table[index]
        prev = None
        
        # Traverse linked list at this index
        while entry is not None:
            if entry.key == key:
                # Found the key - remove it
                if prev is None:
                    # Remove from head
                    self.table[index] = entry.next
                else:
                    # Remove from middle/end
                    prev.next = entry.next
                self.size -= 1
                return entry.value
            prev = entry
            entry = entry.next
        
        return None  # Key not found
    
    def _rehash(self):
        """
        Rehash: double capacity and reinsert all entries
        This maintains O(1) average-case performance
        """
        # Store old table and data
        old_table = self.table
        old_size = self.size
        
        # Create new table with doubled capacity
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        
        # Reinsert all entries into new table
        for entry in old_table:
            while entry is not None:
                self.put(entry.key, entry.value)
                entry = entry.next
    
    def __contains__(self, key):
        """Check if key exists (enables 'key in map' syntax)"""
        return self.get(key) is not None
    
    def __len__(self):
        """Return number of entries"""
        return self.size
    
    def __str__(self):
        """String representation"""
        items = []
        for entry in self.table:
            while entry is not None:
                items.append(f"{entry.key}: {entry.value}")
                entry = entry.next
        return "{" + ", ".join(items) + "}"


# Usage Example:
if __name__ == "__main__":
    # Create HashMap
    my_map = HashMap(capacity=10)
    
    # Put operations
    my_map.put("apple", 5)
    my_map.put("banana", 3)
    my_map.put("cherry", 7)
    
    # Get operations
    print(my_map.get("apple"))   # Output: 5
    print(my_map.get("banana"))  # Output: 3
    print(my_map.get("grape"))   # Output: None
    
    # Contains check
    print("apple" in my_map)      # Output: True
    print("grape" in my_map)      # Output: False
    
    # Remove operations
    my_map.remove("banana")
    print(my_map.get("banana"))   # Output: None
    
    # Size and representation
    print(f"Size: {len(my_map)}")
    print(f"HashMap: {my_map}")
```

---

## Best Practices

### 1. **Hash Function Implementation (Python)**
```python
# Bad: Always returns same value (terrible collisions)
def __hash__(self):
    return 42  # All keys hash to same value!

# Good: Distributes values well using built-in hash()
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    
    def __hash__(self):
        # Use Python's built-in hash on immutable components
        return hash((self.name, self.age, self.email))
    
    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return (self.name == other.name and 
                self.age == other.age and 
                self.email == other.email)
```

### 2. **Equals Method (Python)**
```python
# Must be consistent with __hash__
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age
    
    def __hash__(self):
        # Two equal objects must have same hash
        return hash((self.name, self.age))
```

### 3. **Immutable Keys**
- Use immutable objects as keys (string, int, tuple, frozenset, etc.)
- If key is mutable and modified after insertion, HashMap breaks
```python
# Good
my_map = {}
my_map["apple"] = 5
my_map[42] = "answer"
my_map[(1, 2)] = "tuple key"

# Bad - DON'T DO THIS
key = ["apple"]  # Lists are mutable
my_map[key] = 5  # TypeError: unhashable type: 'list'

# Also bad - Modify after insertion
key = {"a": 1}  # Dictionaries are mutable
my_map[key] = 5  # TypeError: unhashable type: 'dict'
```

### 4. **Handle Null Keys (Python)**
- Python allows None as a key
- Be explicit about None handling in your implementation
```python
my_map = {}
my_map[None] = "null value"
print(my_map[None])  # Output: null value
print(None in my_map)  # Output: True
```

### 5. **Performance Tuning (Python)**
```python
# Bad: Multiple rehashes occur
my_map = {}
for i in range(1000):
    my_map[i] = i  # Rehashing happens multiple times

# Better: Dict grows automatically, Python handles it efficiently
# But for custom HashMap, specify initial capacity:
my_map = HashMap(capacity=2000)  # Avoid multiple rehashes
for i in range(1000):
    my_map.put(i, i)
```

### 6. **Iteration Order (Python)**
- Python 3.7+: dict maintains insertion order
- custom HashMap: order depends on your implementation
- If insertion order matters, use a list or OrderedDict pattern
```python
# Python's built-in dict (ordered since 3.7)
my_map = {}
my_map["apple"] = 1
my_map["banana"] = 2
for key in my_map:  # Insertion order preserved
    print(key)

# Collections.OrderedDict for explicit ordering
from collections import OrderedDict
ordered_map = OrderedDict()
ordered_map["apple"] = 1
ordered_map["banana"] = 2
```

### 7. **Thread Safety (Python)**
- Python dicts are NOT thread-safe
- Use `threading.Lock` for multi-threaded access
- Or use `queue.Queue` for thread-safe operations
```python
import threading

class ThreadSafeHashMap:
    def __init__(self):
        self.map = {}
        self.lock = threading.Lock()
    
    def put(self, key, value):
        with self.lock:
            self.map[key] = value
    
    def get(self, key):
        with self.lock:
            return self.map.get(key)
```

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Average Time Complexity** | O(1) for get/put/remove |
| **Worst Time Complexity** | O(n) when all collisions |
| **Space Complexity** | O(n) |
| **Load Factor Threshold** | 0.75 (typical) |
| **Growth Factor** | 2x (doubling) |
| **Collision Resolution** | Separate chaining (linked list) |
| **Keys** | Should be immutable |
| **Values** | Can be anything, including null |
| **Null Keys** | Usually 1 allowed (implementation-dependent) |

---

## Real-World Applications

1. **Caching**: 
   ```python
   cache = {}  # URL → WebPage
   ```

2. **Frequency Count**: 
   ```python
   word_count = {}  # String → Integer
   ```

3. **LRU Cache**: 
   ```python
   from collections import OrderedDict
   lru_cache = OrderedDict()
   ```

4. **Symbol Tables**: Compiler/Interpreter variable storage

5. **Duplicate Detection**: 
   ```python
   seen = set()  # or use dict
   ```

6. **Grouping**: 
   ```python
   students_by_grade = {}  # Grade → [Students]
   ```

7. **Indexing**: Database index structures

8. **Autocomplete**: 
   ```python
   suggestions = {}  # Prefix → [Suggestions]
   ```

---

**Last Updated**: August 14, 2026
