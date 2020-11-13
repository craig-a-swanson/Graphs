
def earliest_ancestor(ancestors, starting_node):
    pass


# Make starting_node a list and set it to current_path
# Create a stack
# Create a visited set
# Create a dictionary to store lineages {-1:-1}
# Push the current_path onto the stack
# While the size of the stack is greater than zero:
    # Pop the current_path from the stack
    # set the current_node to current_path[-1]
    # Check if the current_node has not been visited
        # Mark the current_node as visited
        # Get the parents of the current_node
        # if get_parents is None
            # store the lineage in the dictionary
            # key is length of path
            # value is current_node
        # for parent in parents:
            # copy the current_path
            # append parent to the copy
            # push the path onto the stack
# Sort (reverse) the dictionary by key and then by value
# Return the first element's value of the dictionary

# GET PARENTS
# Iterate through the array and look to see if tuple[1] is our current_node
# If so, return tuple[0]