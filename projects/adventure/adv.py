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
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
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

traversal_graph = {}
dft_visited = set()
bfs_visited = set()

# travel_direction = ''
last_room = 0
direction_swap = {'n':'s', 'e':'w', 's':'n', 'w':'e'}

# first room set-up
room_exits = player.current_room.get_exits()
room_dict = {}
for exit in room_exits:
    room_dict[exit] = '?'
traversal_graph[player.current_room.id] = room_dict

# Set up the traversal_graph entry for the new room
# for a new room, each exit key is set to a value of '?'
def new_room(from_id, direction):
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
        print(f'this exit is: {exit} and goes to {value}')
        if value == '?':
            travel_direction = exit
            next_location = player.current_room.get_room_in_direction(travel_direction)
            traversal_path.append(travel_direction)
            traversal_graph[room_id][travel_direction] = next_location.id
            return travel_direction


travel_direction = find_next_direction(player.current_room.id)
player.travel(travel_direction)
new_room(last_room,travel_direction)
print(player.current_room.get_exits())
print(traversal_graph)




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
