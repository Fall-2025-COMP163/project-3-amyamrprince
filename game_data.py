"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Amya Ratcliff Prince

AI Usage: helped with debugging and explanations.


This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}

    # read file corrupted file errors go here
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        raise CorruptedDataError(f"Could not read quest file: {e}")
    current_quest = {}
    try:
        # Add a blank line at the end to empty the last quest
        for raw_line in lines + ["\n"]:
            line = raw_line.strip()

            # Blank line = end of one quest block
            if line == "":
                if current_quest:
                    required_fields = [
                        "QUEST_ID",
                        "TITLE",
                        "DESCRIPTION",
                        "REWARD_XP",
                        "REWARD_GOLD",
                        "REQUIRED_LEVEL",
                        "PREREQUISITE",
                    ]
                    for field in required_fields:
                        if field not in current_quest or current_quest[field] == "":
                            raise InvalidDataFormatError(
                                f"Missing field '{field}' in quest."
                            )

                    quest_id = current_quest["QUEST_ID"]

                    # Convert numeric fields
                    try:
                        reward_xp = int(current_quest["REWARD_XP"])
                        reward_gold = int(current_quest["REWARD_GOLD"])
                        required_level = int(current_quest["REQUIRED_LEVEL"])
                    except ValueError as e:
                        raise InvalidDataFormatError(
                            f"Invalid number in quest '{quest_id}'."
                        ) from e

                    # Build normalized quest dict
                    quests[quest_id] = {
                        "quest_id": quest_id,
                        "title": current_quest["TITLE"],
                        "description": current_quest["DESCRIPTION"],
                        "reward_xp": reward_xp,
                        "reward_gold": reward_gold,
                        "required_level": required_level,
                        "prerequisite": current_quest["PREREQUISITE"],
                    }

                    current_quest = {}
                continue

            # Non-blank line - must be KEY: value
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line in quest file: '{line}'")

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise InvalidDataFormatError("Missing key in quest line.")

            current_quest[key] = value

    except InvalidDataFormatError:
        raise
    except Exception as e:
        # anything unexpected while parsing is corrupted
        raise CorruptedDataError(f"Error parsing quest data: {e}")

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    # Try t0 read file at all - corrupted file if this fails
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        raise CorruptedDataError(f"Could not read item file: {e}")

    items = {}
    current_block = []

    try:
        # Add an empty line so the last item doesn’t get skipped
        for raw_line in lines + ["\n"]:
            line = raw_line.strip()

            if line == "":
                # end of an item block
                if current_block:
                    # Use helper to parse one item
                    raw_item = parse_item_block(current_block)

                    item_id = raw_item["ITEM_ID"]

                    # Normalize into the structure used by the rest of the game
                    items[item_id] = {
                        "item_id": item_id,
                        "name": raw_item.get("NAME", item_id),
                        "type": raw_item.get("TYPE", "misc"),
                        "effect": raw_item.get("EFFECT", ""),
                        "cost": raw_item.get("COST", 0),  # already int in parse_item_block
                        "description": raw_item.get("DESCRIPTION", ""),
                    }

                    current_block = []
                continue

            # non-blank line - part of current block
            current_block.append(raw_line)

    except InvalidDataFormatError:
        # Re-raise as-is if parse_item_block complained
        raise
    except Exception as e:
        # Anything unexpected while parsing is corrupted data
        raise CorruptedDataError(f"Error parsing item data: {e}")

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]

    # Check for missing keys
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # Check numeric fields  
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]

    for field in numeric_fields:
        value = quest_dict[field]
        try:
            int(value)
        except ValueError:
            raise InvalidDataFormatError(
                f"Field '{field}' must be a valid number, got '{value}'."
            )

    return True
    

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation

    required_fields = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description"
    ]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")
    # Validate type
    valid_types = {"weapon", "armor", "consumable"}
    item_type = item_dict["type"]
    if item_type not in valid_types:
        raise InvalidDataFormatError(
            f"Invalid item type '{item_type}'. Must be one of: {', '.join(valid_types)}."
        )
    # Validate cost is numeric
    try:
        int(item_dict["cost"])
    except ValueError:
        raise InvalidDataFormatError(
            f"Item cost must be a number, got '{item_dict['cost']}'."
        )

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

    default_quests = (
        "QUEST_ID: sample_quest\n"
        "TITLE: Sample Quest\n"
        "DESCRIPTION: This is a default starter quest.\n"
        "REWARD_XP: 10\n"
        "REWARD_GOLD: 5\n"
        "REQUIRED_LEVEL: 1\n"
        "PREREQUISITE: NONE\n"
    )

    default_items = (
        "ITEM_ID: sample_item\n"
        "NAME: Sample Item\n"
        "TYPE: consumable\n"
        "EFFECT: health:5\n"
        "COST: 5\n"
        "DESCRIPTION: A simple default starter item.\n"
    )

    #create data directory
    data_dir = "data"

    try:
        os.makedirs(data_dir, exist_ok=True)
    except PermissionError:
        print("Error: Cannot create 'data' directory due to permission issues.")
        return

    # Create quests.txt if missing
    quests_path = os.path.join(data_dir, "quests.txt")
    if not os.path.exists(quests_path):
        try:
            with open(quests_path, "w") as f:   
                f.write(default_quests)
        except PermissionError:
            print(f"Error: Cannot write to '{quests_path}' due to permission issues.")

    # Create items.txt if missing
    items_path = os.path.join(data_dir, "items.txt")
    if not os.path.exists(items_path):
        try:
            with open(items_path, "w") as f:  
                f.write(default_items)
        except PermissionError:
            print(f"Error: Cannot write to '{items_path}' due to permission issues.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

    quest_data = {}

    for raw_line in lines:
        line = raw_line.strip()

        # Ignore empty lines just in case
        if line == "":
            continue

        # Must have a KEY: VALUE format
        if ":" not in line:
            raise InvalidDataFormatError(f"Invalid quest line: '{line}'")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "" or value == "":
            raise InvalidDataFormatError(f"Malformed quest line: '{line}'")

        quest_data[key] = value

    # Required fields
    required = [
        "QUEST_ID",
        "TITLE",
        "DESCRIPTION",
        "REWARD_XP",
        "REWARD_GOLD",
        "REQUIRED_LEVEL",
        "PREREQUISITE"
    ]

    for field in required:
        if field not in quest_data:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # Convert numeric values
    try:
        quest_data["REWARD_XP"] = int(quest_data["REWARD_XP"])
        quest_data["REWARD_GOLD"] = int(quest_data["REWARD_GOLD"])
        quest_data["REQUIRED_LEVEL"] = int(quest_data["REQUIRED_LEVEL"])
    except ValueError:
        raise InvalidDataFormatError("Numeric field contains invalid value.")

    return quest_data
    

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_data = {}

    for raw_line in lines:
        line = raw_line.strip()

        # ignores blank lines
        if line == "":
            continue

        # must have KEY: VALUE format
        if ":" not in line:
            raise InvalidDataFormatError(f"Invalid item line: '{line}'")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "" or value == "":
            raise InvalidDataFormatError(f"Malformed item line: '{line}'")

        item_data[key] = value

    # Required fields for items
    required_fields = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST"]

    for field in required_fields:
        if field not in item_data:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # Convert numeric fields
    try:
        item_data["COST"] = int(item_data["COST"])
    except ValueError:
        raise InvalidDataFormatError("COST must be a number.")

    return item_data
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    #Test creating default files
    create_default_data_files()
    
    #Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    #Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

