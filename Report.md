# Optimisation Report

**In this report, I will be going through to how I
have optimised my code on the PageRank algorithms. 
The PageRank algorithms that I will be going
through are stochastic and distribution.**

## Stochastic
```
hit_count = {node: 0 for node in graph}

for x in range(args.repeats):
    current_node = random.choice(list(graph.keys()))
    
    for y in range(args.steps):

        if graph[current_node]:
            current_node = random.choice(graph[current_node])
    
    hit_count[current_node] += 1

ranking = {value: count / args.repeats for value, count in hit_count.items()}

return ranking
```
Calculation took 40.10 seconds.
``` 
hit_count = {node: 0 for node in graph}

current_node = random.choice(list(graph.keys()))

for x in range(args.repeats):
    
    if graph[current_node]:
        current_node = random.choice(graph[current_node])
    else:
        current_node = random.choice(list(graph.keys()))

    hit_count[current_node] += 1

ranking = {value: count / args.repeats for value, count in hit_count.items()}

return ranking  
```
Calculation took 0.47 seconds.

### What I have done to optimise the code:

I firstly defined the current node within the first loop 
which meant that for every iteration, a current node was 
always set. This was not necessary as there are nodes that 
had outer edges. Therefore, this made the algorithm very
inconsistent. What I did instead was define the current node
before the first for loop. Then I used IF and ELSE statements
so that a current node is only selected if it does not have
an outer edge.

However, I was still believed that the algorithm was still
slow since there was a steps loop within the repeats loop.
I was able to remove it which now give an execution time of
0.47 seconds.

## Distribution
```
for x in range(args.steps):
    nodes = list(graph.keys())
    number_of_nodes = len(nodes)
    node_prob = {node: 1 / number_of_nodes
                 for node in nodes}
    next_prob = {node: 0
                 for node in nodes}

    for node in nodes:
        if len(graph[node]) > 0:
            p = node_prob[node] / len(graph[node])            
        else:
            p = 0
        
        for target in graph[node]:
            next_prob[target] = next_prob[target] + p

    node_prob = next_prob
return node_prob  # The probability for each node is returned
```
Calculation took 2.19 seconds.

```
nodes = list(graph.keys())
number_of_nodes = len(nodes)
node_prob = {node: 1 / number_of_nodes
             for node in nodes}

for _ in range(args.steps):
    next_prob = {node: 0
                 for node in nodes}

    for node in nodes:
        if len(graph[node]) > 0:
            p = node_prob[node] / len(graph[node])
        else:
            p = 0

        for target in graph[node]:
            next_prob[target] += p

    node_prob = next_prob
return node_prob  
```
Calculation took 0.10 seconds.

### What I have done to optimise this code:

The first 3 variables (nodes, number_of_nodes, node_prob) within 
the first loop are meant to be fixed. This means that they never 
change and are unnecessary to include within each iteration. 
Therefore, it was more beneficial to define the variables outside 
the loops to increase the execution time.

Also, in the first loop, I used the variable "_" to indicate that
the index is not used. This makes the execution time a lot faster as
the algorithm is aware of the index.

## Progress Bar
Using the progress bar in both algorithms made the calculation take
a lot longer. The purpose of this assignment is to ensure that the 
algorithms are optimised as much as possible, especially in PageRank.
Therefore, I did not import the progress bar in my final 
submission.