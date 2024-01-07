
Recursion / Backtracking
39, 40, 78, 90, 46, 47
Graph Travel - DFS, BFS, Topological Sorting
133, 127, 490, 210, 269
Binary Tree / Binary Search Tree(BST)
94, 236, 297, 102, 314, 98
Binary Search
34, 162, 69, 81
Linked List Manipulation
206, 237, 92, 21, 876, 143
Data Structure
242, 133, 127, 155, 225, 215, 23
Pointer Manipulation
239, 3, 76
Greedy
122, 605
Sorting
Time—O(N log N), Merge Sort—Space O(N), Quick sort, 148
Convert Real Life Problem to Code
146, 1066, 490

simulatenously

Responsiveness in User Interface

Responsiveness acheieved by concurrency
Responsiveness acheieved by Parallelism


illusion
caveat


Context Switch

- Context switch is not cheap, and is the price of multitasking(concurrency)
- Same as we humans when we multitask - Takes time to focus
- Each thread consumes resources in the CPU and Memory
- When we switch to a different thread:
  - Store data for one thread
  - Restore data for another thread

Key Takeaways
- Too many threads - Thrashing, spending more ime in management than real productive work.
- Threads consume less resources than processes.
- Context switching between threads from the same process is cheaper than context switch between different processes.

Threads scheduling - First Come First Serve
- Problem - Long thread can cause starvation
- May cause User Interface threads being unresponsive - Bad User Experience
  
Threads scheduling - Shortest Job First

Threads scheduling - Dynamic Priority
- Using Dynamic Priority, the OS will give preference for Interactive threads

## When to prefer Multithreaded Architecture?
- Prefer if the tasks share a lot of data
- Threads are much faster to to create and destroy
- Switching between threads of the same process is faster(shorter context switches)

## When to prefer Multi-Process Architecture?
- Security and stability are of higher importance
- Tasks are unrelated to each other
