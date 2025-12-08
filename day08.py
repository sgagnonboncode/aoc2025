from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm
from src.grids import TupleGrid2D

PUZZLE_ID = 8
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
# NB_PAIRS = 10

input = read_input(PUZZLE_ID)
NB_PAIRS = 1000


class Position3D(tuple[int, int, int]):
    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

    @property
    def z(self) -> int:
        return self[2]

    def eucledian_distance(self, other: "Position3D") -> float:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        ) ** 0.5


positions: list[Position3D] = []
distance_grid = TupleGrid2D[float]()

for line in input:
    x, y, z = map(int, line.strip().split(","))
    positions.append(Position3D((x, y, z)))

nb_pos = len(positions)

for i in range(0, nb_pos - 1):
    for j in range(i + 1, nb_pos):
        pos1 = positions[i]
        pos2 = positions[j]
        dist = pos1.eucledian_distance(pos2)
        # there is no need to store both i,j and j,i since distance will
        # be the same anyway
        distance_grid[(i, j)] = dist


# sort the grid by value, yielding tuple[tuple[index i, index j], distance]
sorted_values = sorted(distance_grid.items(), key=lambda item: item[1])

networks: list[set[Position3D]] = []
unlinked: set[Position3D] = set(positions)

part1 = 0
steps = 0
last_pair: tuple[Position3D, Position3D] | None = None

# part 2 requires us to link the nodes into a single network
while len(unlinked) > 0 or len(networks) != 1:
    if steps == NB_PAIRS:
        # evaluate PART 1
        networks = sorted(networks, key=lambda net: len(net), reverse=True)
        part1 = len(networks[0]) * len(networks[1]) * len(networks[2])

    (pos_idx1, pos_idx2), dist = sorted_values[steps]
    last_pair = (positions[pos_idx1], positions[pos_idx2])

    # remove from unlinked if not already done
    unlinked.discard(positions[pos_idx1])
    unlinked.discard(positions[pos_idx2])

    # look if any of the positions are already part of networks
    pos1_network = None
    pos2_network = None
    for net in networks:
        if positions[pos_idx1] in net:
            pos1_network = net
        if positions[pos_idx2] in net:
            pos2_network = net

    if pos1_network and pos2_network:
        # merge networks if different, nothing to do otherwise
        if pos1_network != pos2_network:
            pos1_network.update(pos2_network)
            networks.remove(pos2_network)
    elif pos1_network:
        # add to existing network
        pos1_network.add(positions[pos_idx2])
    elif pos2_network:
        # add to existing network
        pos2_network.add(positions[pos_idx1])
    else:
        # create a new network
        new_network = set()
        new_network.add(positions[pos_idx1])
        new_network.add(positions[pos_idx2])
        networks.append(new_network)

    steps += 1

if last_pair is None:
    raise ValueError("Error processing input pairs")

part2 = last_pair[0].x * last_pair[1].x

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
