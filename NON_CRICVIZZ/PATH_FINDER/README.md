# PATH FINDER

A Python-based file searching utility that explores the computer's file system using Depth First Search (DFS).

## Introduction

I developed this program after learning and understanding the concepts of Python Object-Oriented Programming (OOP), the Operating System library (`os`) and the System library (`sys`).

The main objective was to combine these concepts and build a utility that can search for files across the computer's file system.

## Reason Behind Building This

I built this program to make file searching possible through the Command Line Interface (CLI).

It works somewhat like the Windows Search feature, but instead of using a graphical interface, it performs file searching through the terminal.

Another objective was to make the program reusable. It can be executed independently or imported into another Python program as a library.

## Data Structures and Algorithm Concepts Used

The project uses the concept of **Depth First Search (DFS)** in two different ways:

1. Recursive Depth First Search
2. Iterative Depth First Search

Both approaches explore directories and their contents to locate the requested file.

## Depth First Search (DFS)

Depth First Search is a non-heuristic graph traversal and search algorithm.

It starts from a given node and explores one path as deeply as possible before backtracking to explore other paths.

DFS follows the **LIFO (Last In, First Out)** principle when implemented using a stack.

In a file system, directories can be treated as nodes, while files and subdirectories represent their contents.

### 1. Recursive Depth First Search

In recursive DFS, the algorithm relies on the **program's call stack**.

Whenever a directory is encountered, the function calls itself to explore that directory. Once the directory has been explored, the function returns to its previous call and continues searching.

**Pseudocode:**

```text
RECURSIVE_DFS(directory, target):

    FOR each item in directory:

        IF item is a file:
            IF item matches target:
                RETURN item

        ELSE IF item is a directory:
            result = RECURSIVE_DFS(item, target)

            IF result is found:
                RETURN result

    RETURN NOT_FOUND
```

**Working Principle:**

1. Start from the given directory.
2. Read its contents.
3. Check whether an item is the target file.
4. If the item is a directory, recursively enter it.
5. Continue exploring until the file is found or all accessible directories are exhausted.
6. Return to the previous function call through backtracking.

### 2. Iterative Depth First Search

Unlike recursive DFS, iterative DFS does not rely on recursive function calls.

It uses an explicitly maintained **stack data structure** to keep track of directories that need to be explored.

**Pseudocode:**

```text
ITERATIVE_DFS(starting_directory, target):

    CREATE an empty stack
    PUSH starting_directory into stack

    WHILE stack is not empty:

        current_directory = POP stack

        FOR each item in current_directory:

            IF item is a file:
                IF item matches target:
                    RETURN item

            ELSE IF item is a directory:
                PUSH item into stack

    RETURN NOT_FOUND
```

**Working Principle:**

1. Create an empty stack.
2. Push the starting directory into the stack.
3. Pop a directory from the stack.
4. Explore its contents.
5. Push discovered subdirectories into the stack.
6. Repeat until the target file is found or the stack becomes empty.

## Technologies and Libraries Used

- **Python** – Primary programming language.
- **OS** – Used for interacting with the operating system and navigating directories.
- **SYS** – Used for system-related operations.
- **OOP** – Used to organise the program through classes and methods.

## Project Structure

```text
PATH_FINDER/
│
├── path_finder.py
└── README.md
```

## Future Improvements

- Improve searching efficiency.
- Add more searching techniques such as Breadth First Search (BFS).
- Improve handling of inaccessible directories and permission errors.
- Add additional search filters and options.

## Author

**Pradyumna Roy Choudhury**

Developed as a personal Python project while learning Object-Oriented Programming, operating system concepts and data structures and algorithms.