# IDFS (Informed Depth-First Search)

### Introduction
Crossword puzzles are an incredibly popular pastime, providing entertainment to as many as 50 million people in the United States alone. The process of solving a puzzle initially appears to be a uniquely human academic task, leveraging an individual’s vast general knowledge base and a wide range of problem-solving analytical skills, such as assessing which clues are more likely to be correct. However, modern advances in artificial intelligence present the potential to replicate or compete with these skills with algorithmic approaches, making puzzle solving an active field of interest and an intriguing application of AI algorithms.
  
To this end, numerous different approaches to solving a crossword puzzle have been offered exploring various areas of artificial intelligence. While some make use of learning systems such as neural networks, others accumulate a knowledge base to query the given clues. Across the approaches, most techniques often involve some degree of natural language processing to read in the clues, the techniques by which computers can be made to comprehend human language. However, understanding the intention of the clues is only a small (but incredibly challenging) part of the capacity to solve a given crossword puzzle. A computer also needs to support the capability of representing and storing the puzzle, possibly retaining and updating a knowledge base which stores potential guesses to clues, and implement rules to resolve conflicts between two guesses or choose between competing guesses. In this way, crossword puzzle solving is essentially a combination of problems in two key areas: the language processing or semantic problem of finding potential correct answers using the given clues and the spatial or orthographic problem of representing the grid and fitting the words according to its limitations. 
  
This program implements an informed search algorithm is implemented which recursively traverses the solution space, relying on external APIs for information retrieval and implementing collision resolving algorithms and a metric for evaluating the best solution. 

### Repository Structure
- src
  - helper : helpful helper methods
  - metrics : files to measure performance of algorithm
  - model : classes
  - searcher : API interactions
  - **main.py : RUNNABLE**
- test
  - tests.py : test file
- data
  - example Crossword puzzle data
  
### Running the program

Importing relative files is a little bit tricky in Python because of Python's structure with modules, packages, etc. The project has currently been configured to modify `sys.path`. Because of this, in order to run the program, we recommend always staying in the top level directory and executing `python` from there. For instance:

1. To run main.py
```
ark@ark-mbp CrosswordSolver % python3 src/main.py
```
2. To run tests.py
```
ark@ark-mbp CrosswordSolver % python3 test/tests.py
```
3. To run complexity_statistics.py
```
ark@ark-mbp CrosswordSolver % python3 src/metrics/complexity_statistics.py
```


