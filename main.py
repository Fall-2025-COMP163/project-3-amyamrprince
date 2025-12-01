"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3) # used a while loop
    # Return choice

    print("Options:\n")
    print("1.New Game\n")
    print("2.Load Game\n")
    print("3. Exit\n")
    user_input = int(input("Enter your option here "))
    while user_input < 1 or user_input > 3:
        print("Invalid Choice- Please select from the options below\n")
        print("Options:\n")
        print("1.New Game\n")
        print("2.Load Game\n")
        print("3. Exit\n")
        user_input = int(input("Enter your option here "))
    return user_input
    

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character() #note: only accepting int ask chat what can be used to convert back into a string
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop

    try:
        character_name = input("Enter Character name here: ")
    
        print("Choose your Character Class: (1)Warrior, (2)Mage, (3)Rogue")

        character_class = input("Enter Character Class here: ")
        character_classdict = {1:"Warrior", 2:"Mage", 3:"Rogue"}
        character_number = int(character_class)
        if character_number in character_classdict:
            character_key = character_classdict[character_number]#hold charater_class
            
            
        else:
            raise InvalidCharacterClassError("Pick a number 1-3") 
            
            
        current_character = character_manager.create_character(character_name,character_key)
        print("Your Character has been created!")
        print(f"Name:{current_character['name']}")
        print(f"Class:{current_character['class']}")
        print(f"Level: {current_character['level']}")
        print(f"Strength:{current_character['strength']}")
        print(f"Magic:{current_character['magic']}")
        print(f"Health:{current_character['health']}")
        print(f"Experience:{current_character['experience']}")
        print(f"Gold:{current_character['gold']}")
        print(f"Max Health:{current_character['max_health']}")
        print(f"Inventory:{current_character['inventory']}")
        print(f"Active quest:{current_character['active_quest']}")
        print(f"Completed quest:{current_character['completed_quest']}")
        #save character
        character_manager.save_character(current_character)
        print("Your Character has been saved!")
        #starts game loop only if everything above is correct
        game_loop()

    except InvalidCharacterClassError as e:
        print(e)
   

    

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    saved_names = character_manager.list_saved_characters()
    if len(saved_names) == 0:
        print("No saved games found")
        return
    print("Saved Characters:")
    for index, name in enumerate(saved_names, start=1):
        print(f"{index}. {name}")
    choice = int(input("Enter thr number of the character to load:"))
    while choice < 1 or choice > len(saved_names):
        print("Invalid choice. Try again.")
        choice = int(input("Enter thr number of the character to load:"))
    selected_name = saved_names[choice - 1]
    try:
        current_character = character_manager.load_character(selected_name)
        print("Character Loaded Successfully!")
        game_loop()
    except(CharacterNotFoundError,SaveFileCorruptedError):
        print("Error Loading character.")
        return

    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():#while loop and condtionals 
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        p_choice = game_menu()
        if p_choice == 1:
            view_character_stats()
        elif p_choice == 2:
            view_inventory()
        elif p_choice == 3:
            quest_menu()
        elif p_choice == 4:
            explore()
        elif p_choice == 5:
            shop()
        elif p_choice == 6:
            save_game()
            game_running = False

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("Game Menu:")
    print("1. View Character Stats: ")
    print("2. View Inventory: ")
    print("3. Quest Menu: ")
    print("4. Explore (Find Battles): ")
    print("5. Shop: ")
    print("6. Save and Quit: ")
    choice = int(input("Enter your choice:"))
    while choice < 1 or choice > 6:
        print("Invalid Choice. Try again")
        choice = int(input("Enter your choice:"))

    return choice


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
            return#remove later once other stuff is completed 
        elif choice == 2:
            load_game()
            return#remove later once other stuff is completed 
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

