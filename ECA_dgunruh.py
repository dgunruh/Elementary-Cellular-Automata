
# coding: utf-8

# # 3-state nearest neighbor cellular automata
# ## First up will be the code without the use of functions or classes

import random
from matplotlib import pyplot as plt

rule_number = 7518
length = 100
time = 100

# make the initial condition
initial_condition = [random.randint(0, 2) for _ in range(length)]

# create list of neighborhood tuples in lex. order
neighborhoods = [(0, 0), (0, 1), (0, 2), (1, 0),
                 (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

# convert the rule number to ternary
in_ternary = ''
if rule_number == 0:
    in_ternary = '0'
else:
    nums = []
    n = rule_number
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    in_ternary = ''.join(reversed(nums))

# reverse the rule number
in_ternary = in_ternary[::-1]

# pad the rule number with zeros
ternary_length = len(in_ternary)
if ternary_length != 9:
    padding = 9 - ternary_length
    in_ternary = in_ternary + '0' * padding

lookup_table = dict(zip(neighborhoods, in_ternary))

# initialize spacetime field and current configuration
spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

# apply the lookup table to evolve the CA
# for the given number of time steps
for t in range(time):
    new_configuration = []
    for i in range(len(current_configuration)):

        neighborhood = (current_configuration[(i - 1)],
                        current_configuration[i])

        new_configuration.append(int(lookup_table[neighborhood]))

    current_configuration = new_configuration
    spacetime_field.append(new_configuration)

# plot the spacetime field diagram
plt.figure(figsize=(12, 12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()


# ## Now we make the same code, but instead using functions and one class
#
# Let's start by making our core cellular automata class

class ECA(object):
    '''
    3-site nearest neighbor cellular automata simulator
    '''

    def __init__(self, rule_number, initial_condition):

        for i in initial_condition:
            if i not in [0, 1, 2]:
                raise ValueError("initial condition must \
                    be a list of 0s, 1s, and 2s")
        self.lookup_table = self.create_lookup_table(rule_number)
        self.initial = initial_condition
        self.spacetime = [initial_condition]
        self.current_configuration = initial_condition.copy()
        self._length = len(initial_condition)

    def evolve(self, time_steps):
        '''
        Evolve the current configuration a given number of time steps

        Inputs:
        --------------
        time_steps: int
            Positive integer specifying the
            number of time steps to evolve the configuration
        '''

        if time_steps < 0:
            raise ValueError("time_steps must be a non-negative integer")
        # try converting time_steps to an int and
        # raise an error if it can't be done
        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("time_steps must be a non-negative integer")

        # apply the lookup table to evolve the CA
        # for the given number of time steps
        for _ in range(time_steps):
            new_configuration = []
            for i in range(self._length):

                neighborhood = (self.current_configuration[(i - 1)],
                                self.current_configuration[i])

                new_configuration.append(int(self.lookup_table[neighborhood]))

            self.current_configuration = new_configuration
            self.spacetime.append(new_configuration)

    def create_lookup_table(self, rule_number):
        '''
        Create a ternary rule number and use to create our dictionary,
        which maps neighborhoods to values

        Inputs:
        ---------------
        rule_number: int
            Positive integer specifying which rule to use

        Outputs:
        ---------------
        lookup_table: dict
            Dictionary mapping tuple neighborhoods to
            int values (in the range 0-2)
        '''
        # create list of neighborhood tuples in lex. order
        neighborhoods = [(0, 0), (0, 1), (0, 2), (1, 0),
                         (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

        # convert the rule number to ternary
        in_ternary = ''
        if rule_number == 0:
            in_ternary = '0'
        else:
            nums = []
            n = rule_number
            while n:
                n, r = divmod(n, 3)
                nums.append(str(r))
            in_ternary = ''.join(reversed(nums))

        # reverse the rule number
        in_ternary = in_ternary[::-1]

        # pad the rule number with zeros
        ternary_length = len(in_ternary)
        if ternary_length != 9:
            padding = 9 - ternary_length
            in_ternary = in_ternary + '0' * padding

        return dict(zip(neighborhoods, in_ternary))


# Let's now make two additional functions.
# One which will allow us to view what the cellular automata class creates,
# and another which will create our initial condition

def spacetime_diagram(spacetime_field, size=12, colors=plt.cm.Greys):
    '''
    Produces a simple spacetime diagram image
    using matplotlib imshow with 'nearest' interpolation.

    Inputs
    ---------
    spacetime_field: array-like (2D)
        1+1 dimensional spacetime field, given as a 2D array or list of lists.
        Time should be dimension 0;
        so that spacetime_field[t] is the spatial configuration at time t.

    size: int, optional (default=12)
        Sets the square size of the figure: figsize=(size,size)
    colors: matplotlib colormap, optional (default=plt.cm.Greys)
    '''
    plt.figure(figsize=(size, size))
    plt.imshow(spacetime_field, cmap=colors, interpolation='nearest')
    plt.show()


def create_initial_condition(length):
    '''
    Returns a random string of numbers in the range 0-2, of specified length

    Inputs:
    -----------
    length: int
        How long the string needs to be
    '''
    if not isinstance(length, int) or length < 0:
        raise ValueError("input length must be a positive ingeter")
    return [random.randint(0, 2) for _ in range(length)]


# Now let's put it all together
length = 100
time_steps = 100
initial_condition = create_initial_condition(length)
rule_7518 = ECA(7518, initial_condition)
rule_7518.evolve(time_steps)
spacetime_diagram(rule_7518.spacetime)
