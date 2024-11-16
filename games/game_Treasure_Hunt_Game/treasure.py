import msvcrt
from colorama import init, Fore, Style

# Initialize colorama (necessary for Windows)
init()

# Create the 5x5 grid
grid = [
    [{"type": "E", "collected": False}, {"type": "T", "collected": False}, {"type": "O", "collected": False}, {"type": "E", "collected": False}, {"type": "E", "collected": False}],
    [{"type": "E", "collected": False}, {"type": "O", "collected": False}, {"type": "E", "collected": False}, {"type": "T", "collected": False}, {"type": "E", "collected": False}],
    [{"type": "T", "collected": False}, {"type": "E", "collected": False}, {"type": "E", "collected": False}, {"type": "O", "collected": False}, {"type": "E", "collected": False}],
    [{"type": "E", "collected": False}, {"type": "O", "collected": False}, {"type": "T", "collected": False}, {"type": "E", "collected": False}, {"type": "E", "collected": False}],
    [{"type": "E", "collected": False}, {"type": "E", "collected": False}, {"type": "O", "collected": False}, {"type": "E", "collected": False}, {"type": "T", "collected": False}],
]

# Player starting position
player_pos = [0, 0]

# Function to print the grid (hidden treasures, obstacles)
def print_grid(grid, player_pos):
    for r in range(5):
        for c in range(5):
            if [r, c] == player_pos:
                print(Fore.CYAN + "P" + Style.RESET_ALL, end=" ")  # Player position
            elif grid[r][c]["type"] == "O":
                print(Fore.RED + "O" + Style.RESET_ALL, end=" ")  # Obstacle (red)
            elif grid[r][c]["type"] == "T" and not grid[r][c]["collected"]:
                print(Fore.YELLOW + "T" + Style.RESET_ALL, end=" ")  # Treasure (yellow)
            else:
                print(Fore.GREEN + "E" + Style.RESET_ALL, end=" ")  # Empty space (green)
        print()

# Function to get a single key press (Windows)
def get_key():
    while True:
        # Wait for a key press and decode it
        key = msvcrt.getch().decode("utf-8").upper()
        
        # Allow only valid keys (W, A, S, D, Q)
        if key in ['W', 'A', 'S', 'D', 'Q']:
            return key

# Function to move the player
def move_player(player_pos, direction):
    row, col = player_pos
    if direction == "W":  # Move up
        if row > 0:
            row -= 1
    elif direction == "S":  # Move down
        if row < 4:
            row += 1
    elif direction == "A":  # Move left
        if col > 0:
            col -= 1
    elif direction == "D":  # Move right
        if col < 4:
            col += 1
    return [row, col]

# Function to collect treasures
def collect_treasure(grid, player_pos):
    row, col = player_pos
    if grid[row][col]["type"] == "T" and not grid[row][col]["collected"]:
        grid[row][col]["collected"] = True
        print("You found a treasure!")
    elif grid[row][col]["type"] == "O":
        print("You hit an obstacle! Can't move there.")

# Function to check if all treasures are collected
def all_treasures_collected(grid):
    for row in grid:
        for cell in row:
            if cell["type"] == "T" and not cell["collected"]:
                return False
    return True

# Main game loop
def treasure_hunt_game(grid, player_pos):
    while True:
        print("\nCurrent Grid:")
        print_grid(grid, player_pos)
        
        # Ask for a single key press
        print("Move (W: Up, S: Down, A: Left, D: Right, Q: Quit): ")
        move = get_key()
        print(f"\nYou pressed: {move}")  # Feedback for the pressed key
        
        if move == "Q":
            print("You quit the game.")
            break
        
        # Move player and collect treasure
        new_pos = move_player(player_pos, move)
        
        # If new position is an obstacle, don't move
        if grid[new_pos[0]][new_pos[1]]["type"] == "O":
            print("You hit an obstacle! Try a different direction.")
        else:
            player_pos = new_pos
            collect_treasure(grid, player_pos)
        
        # Check if all treasures are collected
        if all_treasures_collected(grid):
            print("Congratulations! You collected all the treasures!")
            break

# Start the game
treasure_hunt_game(grid, player_pos)
