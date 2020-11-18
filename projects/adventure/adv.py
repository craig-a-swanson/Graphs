from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

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

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

 # ------------------------------------------------

dft_stack = Stack()
bfs_queue = Queue()

# store the graph in a dictionary with a format like:
# {0: {'n':1, 's':'?', 'e':4, 'w':'?'}, 1: {'s': 0}}
traversal_graph = {}

# the dft_visited will be a set of room_id
# as we do the dft, we don't really care if there are unexplored exits,
# we just want to keep going down a path.
dft_visited = set()

last_room = 0
# create a dictionary to easily flip the "to" direction and the "from" direction
direction_swap = {'n':'s', 'e':'w', 's':'n', 'w':'e'}

# Set up the traversal_graph entry for the new room
# for a new room, each exit key is set to a value of '?'
def new_room(from_id, direction):
    traversal_path.append(direction)
    this_room = player.current_room
    last_room = this_room.id
    room_exits = this_room.get_exits()
    room_dict = {}
    if this_room.id not in traversal_graph:
        for exit in room_exits:
            room_dict[exit] = '?'
    room_dict[direction_swap[direction]] = from_id
    traversal_graph[this_room.id] = room_dict


# Find next exit to take
# Loop through the room's exits and take the first '?'
def find_next_direction(room_id):
    room_exits = traversal_graph[room_id]
    for exit, value in room_exits.items():
        # print(f'this exit is: {exit} and goes to {value}')
        if value == '?':
            travel_direction = exit
            next_location = player.current_room.get_room_in_direction(travel_direction)
            traversal_graph[room_id][travel_direction] = next_location.id
            return travel_direction

def backtrack_to_unexplored(current_room):
    # This is the BFS part where we are searching for the first '?'
    # The idea is to first create the path to the room with a '?'
    # Then use that path to move the player back to that room.
    # Append the path onto the traversal_path array.
    # Reset the dft_visited array (CHANGE: Do this in calling code block)
    # Finally, pass the new room_id back to the calling statement
    # If it doesn't find any more '?' then False is passed and it's done


    # the bfs_visited will be a set of room_id
    # the search is looking for a '?' in a dict value
    # but the visited set needs only to keep track of the nodes visited during the search
    bfs_visited = set()
    temp_path = []

    bfs_queue.enqueue((current_room, temp_path))

    while bfs_queue.size() > 0:
        dequeued_tuple = bfs_queue.dequeue()
        current_room = dequeued_tuple[0]
        current_id = current_room.id
        current_path = list(dequeued_tuple[1])

        if current_id not in bfs_visited:
            bfs_visited.add(current_id)

            # check the graph of the current room_id
            # iterate through the exit values
            # if any values contain '?' then this is the path we want
            # otherwise continue to neighboring room
            exits = traversal_graph[current_id]
            if '?' in exits.values():
                for direction in current_path:
                    player.travel(direction)
                    traversal_path.append(direction)
                return current_room
            for direction, room in exits.items():
                new_path = list(current_path)
                next_room = current_room.get_room_in_direction(direction)
                new_path.append(direction)
                bfs_queue.enqueue((next_room, new_path))

    return False


# first room set-up
room_exits = player.current_room.get_exits()
room_dict = {}
for exit in room_exits:
    room_dict[exit] = '?'
traversal_graph[player.current_room.id] = room_dict

dft_stack.push(player.current_room.id)

while dft_stack.size() > 0:
    current_id = dft_stack.pop()

    if current_id not in dft_visited:
        dft_visited.add(current_id)
    
        print(f'current dft_visited size: {dft_visited}')
        print(traversal_graph)
        # pick a neighbor (an exit with a '?')
        next_exit = find_next_direction(current_id)
        if next_exit:
            dft_stack.push(player.current_room.get_room_in_direction(next_exit).id)
            player.travel(next_exit)
            new_room(current_id, next_exit)

        # when there are no exits with a '?', then call bfs to backtrack to first unexplored exit
        else:
            backtrack_location = backtrack_to_unexplored(player.current_room)
            if backtrack_location:
                dft_stack.push(backtrack_location.id)
                dft_visited = set()



# travel_direction = find_next_direction(player.current_room.id)
# player.travel(travel_direction)
# new_room(last_room,travel_direction)
# print(player.current_room.get_exits())
print(traversal_graph)
print(traversal_path)



 # ------------------------------------------------


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
