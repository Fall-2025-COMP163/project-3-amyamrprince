"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Amya Ratcliff Prince

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)
import character_manager 
# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    character["inventory"]
    if len(character["inventory"]) >= 20:
        raise InventoryFullError
    character["inventory"].append(item_id)
    return True
    

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    inventory = character["inventory"]
    if item_id not in inventory:
        raise ItemNotFoundError
    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    inventory = character["inventory"]
    if item_id in inventory:
        return True
    else:
        return False
    

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    inventory = character["inventory"]
    count= inventory.count(item_id)
    return count
    

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    
    current_space = len(character["inventory"])
    
    current_space = len(character["inventory"])
    remaining_space = 20- current_space
    return  remaining_space 

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    inventory = character["inventory"]
    current_inventory = inventory.copy()
    inventory.clear() 
    return current_inventory
    

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    #Check if character has the item
    if not has_item(character,item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    #look up item
    if item_id not in item_data:
        raise ItemNotFoundError(f"Item '{item_id}' is not defined in item_data.")
    info_data = item_data[item_id]

    if item_data["type"] != "consumable": 
        raise InvalidItemTypeError("Invalid type, Try again")
    
    effect_str = item_data["effect"]
    stat_name,value_str = effect_str.split(":")
    value = int(value_str)
    apply_stat_effect(character, stat_name, value) #apply effect
    remove_item_from_inventory(character, item_id) #remove item from inventory
    return f"You used {info_data.get('name', item_id)} and gained +{value} {stat_name}."
        

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError
    info = item_data[item_id]
    if info["type"] != "weapon":
        raise InvalidItemTypeError
    current_weapon = character.get("equipped_weapon")

    if current_weapon is not None:
        old_info = item_data[current_weapon]
        effect_str = old_info["effect"]
        stat_name, value = parse_item_effect(effect_str)
        apply_stat_effect(character,stat_name, -value)
        add_item_to_inventory(character, current_weapon)

    effect_str = info["effect"]
    stat_name, value = parse_item_effect(effect_str)
    apply_stat_effect(character, stat_name, value)
    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)
    return (f"Equipped weapon:{item_id}")

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if not has_item(character, item_id):
        raise ItemNotFoundError
    info = item_data[item_id]
    if info["type"] != "armor":
        raise InvalidItemTypeError
    current_armor = character.get("equipped_armor")
    if current_armor is not None:
        old_info = item_data[current_armor]
        effect_str = old_info["effect"]
        stat_name, value = parse_item_effect(effect_str)
        apply_stat_effect(character,stat_name, -value)
        add_item_to_inventory(character, current_armor)

    effect_str = info["effect"]
    stat_name, value = parse_item_effect(effect_str)
    apply_stat_effect(character, stat_name, value)
    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)
    return (f"Equipped armor:{item_id}")
    

def unequip_weapon(character, item_data):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    current_weapon = character.get("equipped_weapon")

    if current_weapon is None:
        return None
    
    info = item_data[current_weapon]

    effect_str = info.get("effect", "")
    if effect_str:
        stat_name, value = parse_item_effect(effect_str)
        apply_stat_effect(character, stat_name, -value)

    try:
        add_item_to_inventory(character, current_weapon)
    except InventoryFullError:   

        if effect_str:
            apply_stat_effect(character, stat_name, value)
        raise
    character["equipped_weapon"] = None
    return current_weapon

    

    

def unequip_armor(character, item_data):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping

    current_armor = character.get("equipped_armor")

    if current_armor is None:
        return None
    
    info = item_data[current_armor]
    #remove stat bonus
    effect_str = info.get("effect", "")
    if effect_str:
        stat_name, value = parse_item_effect(effect_str)
        apply_stat_effect(character, stat_name, -value)
    # Try to add armor back to inventory
    try:
        add_item_to_inventory(character, current_armor)
    except InventoryFullError:
        # If inventory is full, undo stat removal, keep armor equipped
        if effect_str:
            apply_stat_effect(character, stat_name, value)
        raise   
    # Clear equipped armor
    character["equipped_armor"] = None
    return current_armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    item_info = item_data[item_id]
    cost = item_info["cost"]
    if character["gold"] < cost:
        raise InsufficientResourcesError
    if get_inventory_space_remaining(character)<= 0:
        raise InventoryFullError
    else:
        character["gold"] -= cost
        add_item_to_inventory(character, item_id)
    return True 

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    if not has_item(character, item_id):
        raise ItemNotFoundError
    item_info = item_data[item_id]
    cost = item_info["cost"]

    sell_price = cost // 2
    remove_item_from_inventory(character, item_id)
    character["gold"] += sell_price
    return sell_price


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    stat_name, value_str = effect_string.split(":")
    value = int(value_str)
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health

    if stat_name == "health":
        character["health"] = min(character["health"] + value,
                              character["max_health"])
    elif stat_name in character:
        character[stat_name] += value

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character["inventory"]
    items = set(inventory)
    for item_id in items:
        name = item_data_dict[item_id]["name"]
        type_ = item_data_dict[item_id]["type"]
        count = count_item(character, item_id)
        print(f"{name} ({type_}) — x{count}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    #Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    
    try:
        # a,b,c,result = use_item(test_char, "health_potion", test_item)
        # print("this is",a)
        # print(b)
        # print(c)
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

