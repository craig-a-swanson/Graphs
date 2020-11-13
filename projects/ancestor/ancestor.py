class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def get_parents(ancestors, node):
    # Create a set of parents to return
    # Iterate through the ancestors array and look to see if tuple[1] is our current_node
    # If so, add tuple[0] to the parents set
    parents = set()
    for child in ancestors:
        if child[1] == node:
            parents.add(child[0])
    return parents

def earliest_ancestor(ancestors, starting_node):

    # Make starting_node a list and set it to current_path
    current_path = list([starting_node])

    # Create a stack
    # Create a visited set
    # Create a dictionary to store lineages {-1:-1}
    stack = Stack()
    visited = set()
    lineages = {-1:-1}

    # Push the current_path onto the stack
    stack.push(current_path)

    while stack.size() > 0:
        # While the size of the stack is greater than zero:
        # Pop the current_path from the stack
        # set the current_node to current_path[-1]
        current_path = stack.pop()
        current_node = current_path[-1]

        # Check if the current_node has not been visited
        if current_node not in visited:
            # Mark the current_node as visited
            visited.add(current_node)

            # Get the parents of the current_node
            parents = get_parents(ancestors, current_node)
            # if get_parents is None
                # store the lineage in the dictionary
                # value is length of path
                # key is current_node
            if len(parents) == 0 and len(current_path) > 1:
                lineages[current_node] = len(current_path)
            
            for parent in parents:
                # copy the current_path
                # append parent to the copy
                # push the path onto the stack
                new_path = list(current_path)
                new_path.append(parent)
                stack.push(new_path)

    # Sort the dictionary: primary sort by value is reversed, secondary sort by key is not reversed (used -x)
    # Return the first element's value of the dictionary
    sorted_lineage = sorted(lineages.items(), key=lambda x: (x[1], -x[0]), reverse=True)
    return sorted_lineage[0][0]

# test_list = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
# print(earliest_ancestor(test_list, 9))