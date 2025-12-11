from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from colorama import Fore, Back, Style
from tqdm import tqdm
import re
from z3 import Int, Sum, sat, Optimize
from functools import lru_cache


PUZZLE_ID = 11
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

next_index =0
machine_outputs : dict[str, set[str]] = {}

for line in input:
    line = line.strip()
    l_r = line.split(": ")
    machine_name = l_r[0]
    output_names = l_r[1].split(" ")
    machine_outputs[machine_name] = set(output_names)



# now we have a graph of machines and their outputs

# PART 1:
# using dfs, find all UNIQUE paths which start from 'you' and end at 'out'.
# the graph may contain cycles which we want to avoir looping on, 
# so we need to keep track of visited nodes.

def dfs_memoized(current_machine: str, visited_tuple: tuple, target: str) -> int:
    @lru_cache(maxsize=None)
    def _dfs(current: str, visited_frozen: frozenset, target: str):
        if current == target:
            return 1
        
        path_count = 0
        for output_machine in machine_outputs.get(current, []):
            if output_machine not in visited_frozen:
                new_visited = visited_frozen | {output_machine}
                path_count += _dfs(output_machine, new_visited, target)
        return path_count
    
    return _dfs(current_machine, frozenset(visited_tuple), target)


part1 = dfs_memoized("you", ("you",), "out")

# Part 2: find all paths from 'svr' to 'out' which pass through both 'dac' and 'fft' in any order.
# so either srv -> ... -> dac -> ... -> fft -> ... -> out
#        or srv -> ... -> fft -> ... -> dac -> ... -> out

# process in two parts : find all from svr to dac to fft to out , then from svr to fft to dac to out

# first, test if a path exists between 'fft' and 'dac' and vice versa
part2=0

def dfs_path_exists(start: str, end: str, visited: set[str]) -> bool:
    if start == end:
        return True
    
    for neighbor in machine_outputs.get(start, []):
        if neighbor not in visited:
            new_visited = visited | {neighbor}
            if dfs_path_exists(neighbor, end, new_visited):
                return True
    return False

dac_to_fft_exists = dfs_path_exists("dac", "fft", {"dac"})
fft_to_dac_exists = dfs_path_exists("fft", "dac", {"fft"})

print(f"DAC to FFT path exists: {dac_to_fft_exists}")
print(f"FFT to DAC path exists: {fft_to_dac_exists}")

if dac_to_fft_exists:
    # analysis of my input shows that there is no path from DAC to FFT.
    # im not gonna bother deduplicating the logic since its not needed for my puzzle.
    raise ValueError("DAC to FFT does not exist in my input, unexpected")

if not fft_to_dac_exists:
    # analysis of my input shows that there is a path from FFT to DAC.
    raise ValueError("FFT to DAC should exist in my input, unexpected")

# compute an inverse map of which machines can reach which other machines
reachable_map : dict[str, set[str]] = {}
for start,destinations in machine_outputs.items():
    for dest in destinations:
        if dest not in reachable_map:
            reachable_map[dest] = set()
        reachable_map[dest].add(start)

# lets define functions which will help us cull the graph to only nodes that are relevant
def dfs_reachable_from(start:str) -> set[str]:
    reachable_from_start:set[str] = set()
    visited:set[str] = set()

    next_nodes:set[str] = {start}
    while True:
        current_nodes = next_nodes
        next_nodes = set()
        for node in current_nodes:
            if node not in visited:
                visited.add(node)
                reachable_from_start.add(node)
                for neighbor in machine_outputs.get(node, []):
                    if neighbor not in visited:
                        next_nodes.add(neighbor)
        if len(next_nodes) == 0:
            break
    return reachable_from_start

def dfs_can_reach(target:str) -> set[str]:
    can_reach_target:set[str] = set()
    visited = set()
    next_nodes = {target}
    while True:
        current_nodes = next_nodes
        next_nodes = set()
        for node in current_nodes:
            if node not in visited:
                visited.add(node)
                can_reach_target.add(node)
                for neighbor in reachable_map.get(node, []):
                    if neighbor not in visited:
                        next_nodes.add(neighbor)
        if len(next_nodes) == 0:
            break
    return can_reach_target



reachable_from_fft = dfs_reachable_from("fft")
print(f"Nodes reachable from FFT: {len(reachable_from_fft)}")
can_reach_dac = dfs_can_reach("dac")
print(f"Nodes that can reach DAC: {len(can_reach_dac)}")

if 'out' in can_reach_dac:
    print("Out is reachable from DAC")

nodes_from_fft_to_dac = reachable_from_fft.intersection(can_reach_dac)
print(f"Nodes that are both reachable from FFT and can reach DAC: {len(nodes_from_fft_to_dac)}")

def dfs_reachable_from_limited(start:str, end:str, valid_nodes:set[str]) -> int:

    # now, search for all paths from 'fft' to 'dac' that only go through these valid middle nodes
    def dfs_count_paths(current: str, target: str, visited: set[str]) -> int:
        if current == target:
            return 1
        
        path_count = 0
        for neighbor in machine_outputs.get(current, []):
            if neighbor in valid_nodes and neighbor not in visited:
                new_visited = visited | {neighbor}
                path_count += dfs_count_paths(neighbor, target, new_visited)
        return path_count
    
    return dfs_count_paths(start, end, {start})

# make a set of all nodes minus the nodes_from_fft_to_dac
outer_nodes = set(machine_outputs.keys()).union(set(reachable_map.keys())) - nodes_from_fft_to_dac
print("Outer nodes count: ", len(outer_nodes))


# search for all path from 'srv' to 'fft' along those nodes
outer_nodes.add("fft")
srv_to_fft = dfs_reachable_from_limited("svr", "fft", outer_nodes) # 6351
print(f"Number of paths from SVR to FFT through outer nodes: {srv_to_fft}")

fft_to_dac = dfs_reachable_from_limited("fft", "dac", nodes_from_fft_to_dac) # 6788852
print(f"Number of paths from FFT to DAC through valid middle nodes: {fft_to_dac}") 

outer_nodes.remove("fft")
outer_nodes.add("dac")
dac_to_out = dfs_reachable_from_limited("dac", "out", outer_nodes) # 9676
print(f"Number of paths from DAC to OUT through outer nodes: {dac_to_out}")

part2 = srv_to_fft * fft_to_dac * dac_to_out  # 417190406827152


print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
