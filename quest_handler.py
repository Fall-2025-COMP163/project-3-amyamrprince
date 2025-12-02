"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Amya Ratcliff Prince

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
from character_manager import gain_experience, add_gold

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):#use AI to help explain what was being asked
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]
    # Checks level requirement

    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError(f"Requires level {required_level}, but character is level {character.get('level', 1)}.")
    
    # Checks if already completed
    if is_quest_completed(character, quest_id):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")
    
    # Checks if already active
    if is_quest_active(character, quest_id):
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")
    # Checks prerequisite
    prereq_id = quest.get("prerequisite", "NONE")
    if prereq_id != "NONE" and not is_quest_completed(character, prereq_id):
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq_id}' has not been completed.")

    #add to active quests
    active_list = character.setdefault("active_quests", [])
    active_list.append(quest_id)

    return True
    

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest = quest_data_dict[quest_id]
     #check if quest is active
    active_list = character.get("active_quests", [])
    if quest_id not in active_list:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")
    #remove from active quest
    active_list.remove(quest_id)
    #add completed quest
    completed_list = character.setdefault("completed_quests", [])
    if quest_id not in completed_list:
        completed_list.append(quest_id)

    reward_xp = quest.get("reward_xp", 0)
    reward_gold = quest.get("reward_gold", 0)

    #grant rewards
    gain_experience(character, reward_xp) #i had to import gain and add_gold from character_manger
    add_gold(character, reward_gold) 
    
    return {
        "quest_id": quest_id,
        "reward_xp": reward_xp,
        "reward_gold": reward_gold
    }



def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    active = character.get("active_quests", [])
    if quest_id not in active:
        raise QuestNotActiveError(f"Quest:'{quest_id}' is not active.")
    active.remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_ids = character.get("active_quests", [])
    active_list = []
    for q in active_ids:
        if q in quest_data_dict:
            active_list.append(quest_data_dict[q])
    return active_list

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_ids = character.get("completed_quests", [])
    completed_list = []
    for c in completed_ids:
        if c in quest_data_dict:
            completed_list.append(quest_data_dict[c])
    return completed_list
    

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available_list = []
    for quest_id, quest_data in quest_data_dict.item():
        if can_accept_quest(character, quest_id, quest_data_dict):
            available_list.append(quest_data)
    return available_list
   

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get("completed_quests", [])
    

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character.get("active_quests", []) 
    

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
     # Can't already be completed
    if is_quest_completed(character, quest_id):
        return False
    # Can't already be active
    if is_quest_active(character, quest_id):
        return False
    # Check level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        return False
    # Check prerequisite quest (if any)
    prereq_id = quest.get("prerequisite", "NONE")
    if prereq_id != "NONE" and not is_quest_completed(character, prereq_id):
        return False
      # all requirements are met
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    chain = []
    current_id = quest_id
    
    
    while True:
        if current_id not in quest_data_dict:
            # A prerequisite points to a non-existent quest
            raise QuestNotFoundError(f"Quest '{current_id}' not found in prerequisite chain.")
       
        chain.append(current_id)
        
        prereq_id = quest_data_dict[current_id].get("prerequisite", "NONE")

        if prereq_id == "NONE":
            break  # end of chain

        current_id = prereq_id
    chain.reverse()
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    
    completed_quests = len(character.get("completed_quests", []))

    percentage= (completed_quests/ total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    completed_ids = character.get("completed_quests", [])

    for quest_id in completed_ids:
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }
def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    results = []
    for quest_id, quest_data in quest_data_dict.items():
        required_level = quest_data.get("required_level", 1)

        if min_level <= required_level <= max_level:
            results.append(quest_data)

    return results

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data.get['description']}")
    print(f"Required Level: {quest_data.get['required_level', 1]}")

    prereq = quest_data.get("prerequisite", "NONE")
    if prereq != "NONE":
        print(f"Prerequisite: {prereq}")
    else:
        print("Prerequisite: None")
    print(f"Rewards: {quest_data.get('reward_xp', 0)} XP, {quest_data.get('reward_gold', 0)} gold\n")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("\nNo quests to display.\n")
        return
    print("\n=== Available Quests ===")
    for quest in quest_list:
        title = quest.get("title", "Unknown Quest")
        req_level = quest.get("required_level", 1)
        reward_xp = quest.get("reward_xp", 0)
        reward_gold = quest.get("reward_gold", 0)

        print(f"\n• {title}")
        print(f"  Required Level: {req_level}")
        print(f"  Rewards: {reward_xp} XP, {reward_gold} gold")
    

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    # Get active and completed quests 
    active_quests = get_active_quests(character, quest_data_dict)
    completed_quests = get_completed_quests(character, quest_data_dict)

    active_count = len(active_quests)
    completed_count = len(completed_quests)

    completion_pct = get_quest_completion_percentage(character, quest_data_dict)
    totals = get_total_quest_rewards_earned(character, quest_data_dict)
    total_xp = totals["total_xp"]
    total_gold = totals["total_gold"]

    print("\n=== Quest Progress ===")
    print(f"Active quests: {active_count}")
    print(f"Completed quests: {completed_count}")
    print(f"Quest completion: {completion_pct:.1f}%")
    print(f"Total rewards earned from quests: {total_xp} XP, {total_gold} gold")
    

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict

    for quest_id, quest_data in quest_data_dict.items():
        prereq_id = quest_data.get("prerequisite", "NONE")
    if prereq_id != "NONE":
            if prereq_id not in quest_data_dict:
                # prerequisite points to a quest that doesn't exist
                raise QuestNotFoundError(
                    f"Quest '{quest_id}' has invalid prerequisite '{prereq_id}'."
                )

    return True
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

