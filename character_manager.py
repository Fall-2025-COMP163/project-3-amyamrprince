"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Amya Ratcliff Prince]

AI Usage: helped with correcting key mismatches and debugging character_manager errors.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    character_level = 1
    character_experience = 0
    character_gold = 100
    if character_class == "Warrior":
        character_health = 120
        character_strength = 15
        character_magic = 5
    elif character_class == "Mage":
        character_health = 80
        character_strength = 8
        character_magic = 20
    elif character_class == "Rogue":
        character_health = 90
        character_strength = 12
        character_magic = 10
    elif character_class == "Cleric":
        character_health = 100
        character_strength = 10
        character_magic = 15 
    
    else:
        raise InvalidCharacterClassError("Invalid class")
    max_health = character_health
    inventory = []
    active_quests = []
    completed_quests = []


    character_dictionary = {"name": name,
                       "class": character_class,
                       "level": character_level,
                       "strength": character_strength,
                       "magic": character_magic,
                       "health": character_health,
                       "experience":character_experience,
                       "gold": character_gold,
                       "max_health": max_health,
                       "inventory": inventory,
                       "active_quests": active_quests,
                       "completed_quests": completed_quests}
    return character_dictionary

    
    

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

    #Make sure the save directory exists and is a folder
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)
#converts the list into a string
    inventory_str = ",".join(character.get("inventory",[]))
    active_str = ",".join(character.get("active_quests",[]))
    completed_str = ",".join(character.get("completed_quests",[]))

    with open(filepath,"w") as f:
        f.write(f"NAME:{character['name']}\n")
        f.write(f"CLASS:{character['class']}\n")
        f.write(f"LEVEL:{character['level']}\n")
        f.write(f"HEALTH:{character['health']}\n")
        f.write(f"MAX_HEALTH:{character['max_health']}\n")
        f.write(f"STRENGTH:{character['strength']}\n")
        f.write(f"MAGIC:{character['magic']}\n")
        f.write(f"EXPERIENCE:{character['experience']}\n")
        f.write(f"GOLD:{character['gold']}\n")
        f.write(f"INVENTORY:{inventory_str}\n")
        f.write(f"ACTIVE_QUESTS:{active_str}\n")
        f.write(f"COMPLETED_QUESTS:{completed_str}\n")
    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = (f"{character_name}_save.txt")
    filepath = os.path.join(save_directory,filename)
    if not os.path.isfile(filepath):
        raise CharacterNotFoundError
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except:
        raise SaveFileCorruptedError
    character = {}
    for line in lines:
        key, value = line.split(":",1)
        key = key.strip()
        value = value.strip()
        if key == "NAME":
            character["name"] = value
        elif key == "CLASS":
            character["class"] = value
        elif key == "LEVEL":
            character['level'] = int(value)
        elif key == "HEALTH":
            character["health"] = int(value)
        elif key == "MAX_HEALTH":
            character["max_health"] = int(value)
        elif key == "STRENGTH":
            character["strength"] = int(value)
        elif key == "MAGIC":
            character["magic"] = int(value)
        elif key == "EXPERIENCE":
            character["experience"] = int(value)
        elif key == "GOLD":
            character["gold"] = int(value)
        elif key == "INVENTORY":
            if value == "":
                character["inventory"] = []
            else:
                character["inventory"] = value.split(",")
        elif key == "ACTIVE_QUESTS":
            if value == "":
                character["active_quests"] = []
            else:
                character["active_quests"] = value.split(",")   
        elif key == "COMPLETED_QUESTS":
            if value == "":
                character["completed_quests"] = []
            else:
                character["completed_quests"] = value.split(",") 
    #print("Debug keys:",character.keys()) 
    validate_character_data(character)
    return character
    

    


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    saved_names = [] 
    if not os.path.isdir(save_directory): #checking if directory exist
        return saved_names
    
    files = os.listdir(save_directory) #gives list of filenames
    for filename in files: #checks each file
        if filename[-9:] == "_save.txt": # identify files that have _save.txt" at the end
            name = filename[:-9] # remove "_save.txt" to get the character name
            saved_names.append(name) # add name to the results list
    return saved_names
        


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = (f"{character_name}_save.txt")
    filepath = os.path.join(save_directory,filename)
    if not os.path.isfile(filepath):
        raise CharacterNotFoundError
    else:
        os.remove(filepath)
        return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if is_character_dead(character) == True:
        raise CharacterDeadError
    character["experience"] += xp_amount
    player_xp = character["level"] * 100
    while character["experience"]>= player_xp:
        character["experience"] -= player_xp
        character["level"]+= 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        player_xp = character["level"] * 100

    pass

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    current_gold = character["gold"]
    new_gold = current_gold + amount
    if new_gold <0:
        raise ValueError("Gold cannot be negavtive.")
    character["gold"] = new_gold
    return new_gold


    

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    old_health = character["health"]
    new_health = min(old_health + amount, character["max_health"])
    character["health"] = new_health
    heald_amount = new_health - old_health
    return heald_amount
    

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    if character["health"] <= 0:
        return True
    else:
        return False

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if character["health"] > 0:
        return False
    else:
        half_health = character["max_health"] // 2
        final_health = max(half_health,1)
        character["health"] = final_health
        return True
    

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    if not isinstance(character,dict):
        raise InvalidSaveDataError("Character data has to be a dictionary")
    
    required_fields = [ "name", "class", "level", "health","max_health", 
                    "strength", "magic", "experience", "gold", "inventory",
                    "active_quests", "completed_quests"]
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError("Charater is missing a field")
        
        if  not isinstance(character["name"],str):
            raise InvalidSaveDataError
        if not isinstance(character["class"],str):
            raise InvalidSaveDataError
    int_fields = ["level", "health","max_health", "strength", "magic", "experience","gold"]
    for f in int_fields:
        if not isinstance(character[f], int):
            raise InvalidSaveDataError
    list_fields = ["inventory","active_quests","completed_quests"] 
    for l in list_fields:
        if not isinstance(character[l], list):
            raise InvalidSaveDataError  
        
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    
    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
         print(f"Invalid class: {e}")
    
    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")

    # Test deleting
    try:
        delete_character("TestHero")
        print("Delete worked!")
    except CharacterNotFoundError:
        print("Character not found when trying to delete")

