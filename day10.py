from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from colorama import Fore, Back, Style
from tqdm import tqdm
import re
from z3 import Int, Sum, sat, Optimize


PUZZLE_ID = 10
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

class ButtonCombination(list[int]):
    pass

class Machine():
    def __init__(self, ignition_state:list[bool], 
                 buttons: list[ButtonCombination], joltages: list[int]):
        self.nb_lights = len(ignition_state)
        self.ignition_value: list[bool] = ignition_state
        self.buttons = buttons
        self.joltages = joltages
        
        
    def solve_ignition_length(self)->int:
        # the problem is equivalent to trying to solve a system of boolean equations:
        #
        # Example:
        # 
        # .##. : desired state
        # ---------------------
        # ***# : button 1 (3)
        # *#*# : button 2 (1,3)
        # **#* : button 3 (2)
        # **## : button 4 (2,3)
        # #*#* : button 5 (0,2)
        # ##** : button 6 (0,1)
        #
        # every light can be reduced to a boolean equation mapped to the buttons that toggle it.
        # for that same example:
        # light 0 (0) = button5 | button6
        # light 1 (1) = button2 | button6
        # light 2 (1) = button3 | button4 | button5
        # light 3 (0) = button1 | button2 | button4
        # with the value of a button being 1 if pressed odd number of times, 0 if even number of times.
        # pressing a button twice in this case is equivalent to not pressing it at all

        # these equations are the constraints we need to satisfy to reach the desired ignition state.
        #
        # we can map each button to a bit in an integer and iterate over all possible combinations
        # keeping the one with the shortest number of pressed buttons.
        constraints: list[tuple[set[int], bool]] = []
        for light_index in range(self.nb_lights):
            toggling_buttons = set()
            for button_index, button in enumerate(self.buttons):
                if light_index in button:
                    toggling_buttons.add(button_index)
            constraints.append( (toggling_buttons, self.ignition_value[light_index]) )



        min_pressed = len(self.buttons) *2
    
        for button_state in range(0, 2**len(self.buttons)):
            # count the number of '1' bits in button_state
            nb_pressed = bin(button_state).count("1")
            if nb_pressed >= min_pressed:
                # dont bother evaluating this state, we already have a better one
                continue

            # evaluate this button state against the constraints
            valid = True
            for (toggling_buttons, desired_light_state) in constraints:
                light_state = False
                for b in toggling_buttons:
                    if (button_state & (1 << b)) != 0:
                        light_state = not light_state
                if light_state != desired_light_state:
                    valid = False
                    break
            if valid:
                # print(f"  Valid button state found: {bin(button_state)} with {nb_pressed} buttons pressed")
                min_pressed = nb_pressed

        return min_pressed
    
    def solve_joltage_length(self)->int:
        # same thing as part1, but its no longer a boolean system but an integer one
        # example:
        # 3 5 4 7 : desired state
        # ---------------------
        # 0 0 0 1 : button 1 (3)
        # 0 1 0 1 : button 2 (1,3)
        # 0 0 1 0 : button 3 (2)
        # 0 0 1 1 : button 4 (2,3)
        # 1 0 1 0 : button 5 (0,2)
        # 1 1 0 0 : button 6 (0,1)
        #
        # every joltage position can be reduced to the following constraints
        # 3 = button5 + button6
        # 5 = button2 + button6
        # 4 = button3 + button4 + button5
        # 7 = button1 + button2 + button4
        # with the value of each buttons being the number of presses
        #
        # or, in matrix form: AX = B:
        #
        # A= | 0 0 0 0 1 1| X = |b1| B = | 3 |
        #    | 0 1 0 0 0 1|     |b2|     | 5 |
        #    | 0 0 1 1 1 0|     |b3|     | 4 |
        #    | 1 1 0 1 0 0|     |b4|     | 7 |
        #                       |b5|     
        #                       |b6|     
        #
        # also, we know that the absolute minimum number of button presses
        # is at least equal to the maximum value in B. (at least 7 in the example)
        #
        # finally, the problem dosent ask us for the exact button presses, just the minimum number
        # of presses to reach the desired joltage state.
        #
        # iterating over all possible combinations at once is too expensive
        # 

        constraints: list[tuple[set[int], int]] = []
        for joltage_index in range(self.nb_lights):
            toggling_buttons = set()
            for button_index, button in enumerate(self.buttons):
                if joltage_index in button:
                    toggling_buttons.add(button_index)
            constraints.append( (toggling_buttons, self.joltages[joltage_index]) )

        constraints = sorted(constraints, key=lambda c: len(c[0]))
        nb_buttons = len(self.buttons)        
        absolute_minimum_presses = max( (j for j in self.joltages) )
        
        # this is an integer linear programming problem (LPP).
        # the variable to optimize is the total number of button presses, as low as possible
        # while satisfying all the constraints of the system.
        #
        # there is bound to be a solution involving modulos of the remaining buttons
        # for the weights of each buttons ... but there is also a nifty library called 'z3-solver'
        # which is perfect for this kind of thing.

        opt = Optimize()
        # b0, b1, b2, ...
        button_vars = [ Int(f"b{b}") for b in range(nb_buttons) ]
        total_presses_var = Int("tp")
        
        opt.add( total_presses_var == Sum( [ button_vars[b] for b in range(nb_buttons) ] ) )
        opt.add( total_presses_var >= absolute_minimum_presses)
        opt.minimize( total_presses_var )

        # add each constraint to the solver
        for (toggling_buttons, desired_joltage) in constraints:
            opt.add( Sum( [ button_vars[b] for b in toggling_buttons ] ) == desired_joltage )

        # add a constraint that no button can be pressed negative times
        for b in range(nb_buttons):
            opt.add( button_vars[b] >= 0 )

        if opt.check() == sat:
            model = opt.model()
            return model.evaluate(total_presses_var).as_long()
        
        raise Exception("No solution found, this should not happen")

       

        

        
IGNITION_REGEX = re.compile(r"[#.]+")
BUTTONS_REGEX = re.compile(r"\([0-9\,]*\)")
JOLTAGE_REGEX = re.compile(r"\{[0-9\,]*\}")

machines: list[Machine] = []

for line in input:
    raw_ignitions = IGNITION_REGEX.findall(line)
    raw_buttons = BUTTONS_REGEX.findall(line)
    raw_joltages = JOLTAGE_REGEX.findall(line)
    ignition_state = [ c == "#" for c in raw_ignitions[0].strip() ]
    buttons = [ ButtonCombination(map(int, btn.strip("()").split(","))) for btn in raw_buttons ]
    joltages = [int(j) for j in raw_joltages[0].strip("{}").split(",")]
    machine = Machine(ignition_state=ignition_state, buttons=buttons, joltages=joltages)
    machines.append(machine)


max_lights = max( (m.nb_lights for m in machines) )

part1=0
part2=0

with tqdm(total=len(machines)) as pbar:
    for i,machine in enumerate(machines):
        part1 += machine.solve_ignition_length()
        part2 += machine.solve_joltage_length()
        pbar.update(1)

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
