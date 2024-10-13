import sys, os

current_dir = os.path.dirname(__file__)

# Navigate up one level from the current script's directory
parent_dir = os.path.dirname(current_dir)

# Define the directory you want to add to sys.path
target_dir = os.path.join(parent_dir, 'config')

sys.path.append(target_dir)

print("Current sys.path:")
for path in sys.path:
    print(path)