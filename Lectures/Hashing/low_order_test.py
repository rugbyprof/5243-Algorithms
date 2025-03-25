import sys
sys.path.append('/usr/local/env/.venv/bin')
from rich import print 
import random

def print_binary_numbers(mod_value,nums=100):
    binary_values = []
    collisions = {}
    """Prints 100 integers in 16-bit binary after applying modulus operation."""
    for i in range(nums):
        modded_value = random.randint(mod_value,mod_value*10) % mod_value # Apply modulus operation
        if not modded_value in collisions:
            collisions[modded_value] = 0
        else:
            print(f"Collision: {modded_value}")
            collisions[modded_value] += 1

        binary_value = format(modded_value, '016b')  # Convert to 16-bit binary
        binary_values.append(binary_value)
        print(f"{i} % {mod_value} = {modded_value} -> Binary: {binary_value}")
    return binary_values, collisions


if __name__ == "__main__":
    # Get input value from user
    if len(sys.argv) == 3:
        mod_value = int(sys.argv[1])
        nums = int(sys.argv[2])
    else:
        mod_value = 16
        nums = 100

    binary_nums,collisions = print_binary_numbers(mod_value,nums)
    print(sorted(binary_nums))
    print(collisions)