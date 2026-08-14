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

**Example:**
```
HashMap<String, Integer> map = new HashMap<>();
map.put("apple", 5);      // Store key-value pair
int value = map.get("apple");  // Retrieve value: 5
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

### Optimal Load Factor:

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

### Implementation Overview:

```
class HashMap<K, V> {
    
    // Internal structure
    private Entry<K, V>[] table;      // Array of buckets
    private int capacity;              // Current capacity
    private int size;                  // Number of entries
    private double loadFactor;         // Load factor threshold (0.75)
    
    // Constructor
    HashMap(int initialCapacity) {
        this.capacity = initialCapacity;
        this.table = new Entry[capacity];
        this.size = 0;
        this.loadFactor = 0.75;
    }
    
    // Put operation
    V put(K key, V value) {
        // Check if rehash needed
        if (size / capacity >= loadFactor) {
            rehash();
        }
        
        // Compute index
        int index = hash(key);
        
        // Handle collision with linked list
        Entry<K, V> entry = table[index];
        while (entry != null) {
            if (entry.key.equals(key)) {
                entry.value = value;  // Update existing
                return;
            }
            entry = entry.next;
        }
        
        // Insert new entry at head
        Entry<K, V> newEntry = new Entry<>(key, value, table[index]);
        table[index] = newEntry;
        size++;
    }
    
    // Get operation
    V get(K key) {
        int index = hash(key);
        Entry<K, V> entry = table[index];
        
        while (entry != null) {
            if (entry.key.equals(key)) {
                return entry.value;
            }
            entry = entry.next;
        }
        return null;  // Not found
    }
    
    // Remove operation
    V remove(K key) {
        int index = hash(key);
        Entry<K, V> entry = table[index];
        Entry<K, V> prev = null;
        
        while (entry != null) {
            if (entry.key.equals(key)) {
                if (prev == null) {
                    table[index] = entry.next;
                } else {
                    prev.next = entry.next;
                }
                size--;
                return entry.value;
            }
            prev = entry;
            entry = entry.next;
        }
        return null;  // Not found
    }
    
    // Hash function
    private int hash(K key) {
        if (key == null) return 0;
        return Math.abs(key.hashCode()) % capacity;
    }
    
    // Rehashing
    private void rehash() {
        Entry<K, V>[] oldTable = table;
        capacity *= 2;  // Double capacity
        table = new Entry[capacity];
        size = 0;
        
        // Reinsert all entries
        for (Entry<K, V> entry : oldTable) {
            while (entry != null) {
                put(entry.key, entry.value);
                entry = entry.next;
            }
        }
    }
    
    // Entry node for linked list
    private static class Entry<K, V> {
        K key;
        V value;
        Entry<K, V> next;
        
        Entry(K key, V value, Entry<K, V> next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }
}
```

---

## Best Practices

### 1. **Hash Code Implementation**
```java
// Bad: Always returns same value (terrible collisions)
@Override
public int hashCode() {
    return 42;
}

// Good: Distributes values well
@Override
public int hashCode() {
    return Objects.hash(name, age, email);
}
```

### 2. **Equals Method**
```java
// Must be consistent with hashCode
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Person)) return false;
    Person person = (Person) o;
    return age == person.age && 
           Objects.equals(name, person.name) &&
           Objects.equals(email, person.email);
}
```

### 3. **Immutable Keys**
- Use immutable objects as keys (String, Integer, etc.)
- If key is mutable and modified after insertion, HashMap breaks
```java
// Good
HashMap<String, Integer> map = new HashMap<>();

// Bad - DON'T DO THIS
StringBuilder key = new StringBuilder("apple");
map.put(key, 5);
key.append("pie");  // Modifying key! Hash changes!
map.get("apple");   // Doesn't find it!
```

### 4. **Handle Null Keys**
- Java HashMap allows one null key
- Decide on your null-handling strategy upfront

### 5. **Performance Tuning**
```java
// Specify initial capacity to avoid multiple rehashes
HashMap<String, Integer> map = new HashMap<>(1000);  // Better than default

// Instead of adding 1000 elements one by one (causes multiple rehashes)
```

### 6. **Iteration Order**
- HashMap iteration order is not guaranteed
- Use LinkedHashMap if insertion order matters
- Use TreeMap if sorted order matters

### 7. **Thread Safety**
- HashMap is NOT thread-safe
- Use ConcurrentHashMap for multi-threaded access
- Or synchronize externally

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

1. **Caching**: Cache<URL, WebPage>
2. **Frequency Count**: Count<String, Integer>
3. **LRU Cache**: LinkedHashMap-based with eviction
4. **Symbol Tables**: Compiler/Interpreter variable storage
5. **Duplicate Detection**: First occurrence finding
6. **Grouping**: Group students by grade
7. **Indexing**: Database index structures
8. **Autocomplete**: Prefix → List of suggestions

---

**Last Updated**: August 14, 2026
