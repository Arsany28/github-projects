import time

# Game state
total_score = 10  # Starting score
high_score = 0
game_over = False
WIN_THRESHOLD = 100
LOSE_THRESHOLD = 0

def show_message(message):
    """Show a message with natural pauses"""
    print("\n" + message)
    time.sleep(1.2 if len(message) < 60 else 1.8)

def get_player_choice(options):
    """Get player input in a friendly way"""
    while True:
        choice = input("\nEnter your choice (number): ").strip()
        if choice in options:
            return choice
        print(f"Please enter a number between 1-{len(options)}")

def show_score():
    """Display the current score in a friendly way"""
    print(f"\n=== Current Resources: {total_score} (Goal: {WIN_THRESHOLD}) ===")
    if total_score >= WIN_THRESHOLD * 0.75:
        print("You're doing great! The colony believes in you!")
    elif total_score <= WIN_THRESHOLD * 0.25:
        print("The colony is worried... you need more resources!")
    time.sleep(1)

def start_game():
    """Begin the adventure with a warm welcome"""
    global total_score, game_over, high_score

    # Reset game state
    total_score = 10
    game_over = False

    show_message("Welcome, brave Space Explorer!")
    show_message("You've landed on the mysterious planet Xenthara-5...")
    show_message("A rogue AI threatens the nearby colony, and you're their last hope!")
    show_message(f"Collect resources (reach {WIN_THRESHOLD} points) to save them!")
    show_message("But be careful - if your resources drop to 0, the mission fails!")

    show_score()
    adventure_loop()

def adventure_loop():
    """Main game loop where choices are made"""
    global total_score, game_over, high_score

    while not game_over:
        show_message("\nWhere should we explore next?")
        print("1. The glowing alien jungle")
        print("2. The crashed freighter wreckage")
        print("3. The unstable lava caves")
        print("4. Return to base (quit)")

        choice = get_player_choice(["1", "2", "3", "4"])

        if choice == "4":
            show_message("Returning to base camp...")
            game_over = True
            break

        if choice == "1":
            explore_jungle()
        elif choice == "2":
            investigate_freighter()
        elif choice == "3":
            descend_caves()

        # Update high score
        if total_score > high_score:
            high_score = total_score

        show_score()

        # Check win/lose conditions
        if total_score >= WIN_THRESHOLD:
            celebrate_victory()
            game_over = True
        else:
            show_message("❌ You have lost the game. Better luck next time.")
            mourn_defeat()
            game_over = True

    offer_replay()

def explore_jungle():
    """Jungle exploration scenario"""
    global total_score

    show_message("\nYou enter the bioluminescent jungle...")
    show_message("The air hums with strange energy as glowing plants pulse around you.")
    print("\nChoose your action:")
    print("1. Search for ancient ruins (risky but potentially rewarding)")
    print("2. Follow the animal sounds (dangerous but interesting)")
    print("3. Stay on the safe path (guaranteed small reward)")

    action = get_player_choice(["1", "2", "3"])

    if action == "1":
        print("\nWhat do you focus on in the ruins?")
        print("1. The glowing artifacts (high risk/reward)")
        print("2. The ancient writings (medium risk/reward)")
        print("3. The structural remains (low risk/reward)")

        focus = get_player_choice(["1", "2", "3"])

        if focus == "1":
            points = 75
            show_message("\nYou successfully extract powerful alien tech! +75 resources")
            total_score += points
        elif focus == "2":
            points = 40
            show_message("\nYou decode valuable information! +40 resources")
            total_score += points
        else:
            points = 20
            show_message("\nYou find some salvageable materials. +20 resources")
            total_score += points

    elif action == "2":
        print("\nHow do you approach the animals?")
        print("1. Try to communicate (requires skill)")
        print("2. Observe from a distance (safe)")
        print("3. Attempt to capture one (dangerous)")

        approach = get_player_choice(["1", "2", "3"])

        if approach == "1":
            points = 50
            show_message("\nThe animals lead you to a hidden cache! +50 resources")
            total_score += points
        elif approach == "2":
            points = 25
            show_message("\nYou learn valuable behavioral patterns. +25 resources")
            total_score += points
        else:
            points = -30
            show_message("\nThe animals turn hostile! You lose 30 resources escaping!")
            total_score += points

    else:
        print("\nWhich safe path do you take?")
        print("1. The northern route (better view)")
        print("2. The eastern route (shorter path)")
        print("3. The southern route (most protected)")

        path = get_player_choice(["1", "2", "3"])

        if path == "1":
            points = 15
            show_message("\nYou spot resources from the high ground. +15 resources")
            total_score += points
        elif path == "2":
            points = 10
            show_message("\nYou find some basic supplies. +10 resources")
            total_score += points
        else:
            points = 5
            show_message("\nYou take the safest route. +5 resources")
            total_score += points

def investigate_freighter():
    """Crashed ship scenario"""
    global total_score

    show_message("\nThe wrecked freighter creaks ominously as you approach...")
    print("\nChoose your action:")
    print("1. Search for survivors (potentially helpful)")
    print("2. Look for supplies (generally safe)")
    print("3. Check the engine room (dangerous but valuable)")

    action = get_player_choice(["1", "2", "3"])

    if action == "1":
        print("\nWhere do you search for survivors?")
        print("1. The bridge (most likely location)")
        print("2. The crew quarters (possible survivors)")
        print("3. The cargo hold (unlikely but possible)")

        location = get_player_choice(["1", "2", "3"])

        if location == "1":
            points = 40
            show_message("\nYou find the captain who shares valuable intel! +40 resources")
            total_score += points
        elif location == "2":
            points = 25
            show_message("\nYou rescue two crew members who assist you. +25 resources")
            total_score += points
        else:
            points = -15
            show_message("\nYou find no one and waste time searching. -15 resources")
            total_score += points

    elif action == "2":
        print("\nWhich supplies do you prioritize?")
        print("1. Medical supplies (most valuable)")
        print("2. Food rations (generally useful)")
        print("3. Tools and equipment (versatile)")

        supplies = get_player_choice(["1", "2", "3"])

        if supplies == "1":
            points = 35
            show_message("\nYou find advanced medical kits! +35 resources")
            total_score += points
        elif supplies == "2":
            points = 25
            show_message("\nYou gather nutritious food stores. +25 resources")
            total_score += points
        else:
            points = 20
            show_message("\nYou collect useful tools. +20 resources")
            total_score += points

    else:
        print("\nHow do you approach the engine room?")
        print("1. Carefully disable safety protocols (risky)")
        print("2. Use protective equipment (safe but slow)")
        print("3. Quick in-and-out approach (balanced)")

        approach = get_player_choice(["1", "2", "3"])

        if approach == "1":
            points = 60
            show_message("\nYou extract the core energy source! +60 resources")
            total_score += points
        elif approach == "2":
            points = 30
            show_message("\nYou safely recover some components. +30 resources")
            total_score += points
        else:
            points = -40
            show_message("\nThe unstable reactor damages your gear! -40 resources")
            total_score += points

def descend_caves():
    """Lava cave scenario"""
    global total_score

    show_message("\nThe caves glow with molten rivers beneath your feet...")
    print("\nChoose your action:")
    print("1. Mine for crystals (requires skill)")
    print("2. Explore deeper (dangerous but rewarding)")
    print("3. Set up sensors (safe information gathering)")

    action = get_player_choice(["1", "2", "3"])

    if action == "1":
        print("\nWhich mining technique do you use?")
        print("1. Precision laser extraction (high yield)")
        print("2. Traditional tools (medium yield)")
        print("3. Basic collection (low yield)")

        technique = get_player_choice(["1", "2", "3"])

        if technique == "1":
            points = 50
            show_message("\nYou extract flawless crystals! +50 resources")
            total_score += points
        elif technique == "2":
            points = 30
            show_message("\nYou gather good quality crystals. +30 resources")
            total_score += points
        else:
            points = 15
            show_message("\nYou collect some basic crystals. +15 resources")
            total_score += points

    elif action == "2":
        print("\nHow deep do you venture?")
        print("1. Just past the first chamber (safe)")
        print("2. To the middle levels (moderate risk)")
        print("3. All the way to the core (extremely dangerous)")

        depth = get_player_choice(["1", "2", "3"])

        if depth == "1":
            points = 20
            show_message("\nYou find some surface deposits. +20 resources")
            total_score += points
        elif depth == "2":
            points = 45
            show_message("\nYou discover a rich vein of minerals! +45 resources")
            total_score += points
        else:
            points = -50
            show_message("\nThe extreme heat damages your equipment! -50 resources")
            total_score += points

    else:
        print("\nWhat type of scan do you perform?")
        print("1. Deep mineral scan (most informative)")
        print("2. Thermal mapping (good information)")
        print("3. Basic survey (quick results)")

        scan = get_player_choice(["1", "2", "3"])

        if scan == "1":
            points = 40
            show_message("\nYour scan reveals valuable deposits! +40 resources")
            total_score += points
        elif scan == "2":
            points = 25
            show_message("\nYou identify promising areas. +25 resources")
            total_score += points
        else:
            points = 15
            show_message("\nYou get basic resource readings. +15 resources")
            total_score += points

def celebrate_victory():
    """Show victory celebration"""
    show_message("\n★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★")
    show_message("CONGRATULATIONS SPACE EXPLORER!")
    show_message(f"You collected {total_score} resources!")
    show_message("The colony is saved thanks to your bravery!")
    show_message("★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★")

def mourn_defeat():
    """Show defeat message"""
    show_message("\n☠ ✖ ☠ ✖ ☠ ✖ ☠ ✖ ☠")
    show_message("MISSION FAILED...")
    show_message("The colony couldn't survive without enough resources.")
    show_message("Better luck next time, explorer.")
    show_message("☠ ✖ ☠ ✖ ☠ ✖ ☠ ✖ ☠")

def offer_replay():
    """Ask if player wants to play again"""
    global high_score

    show_message(f"\nYour highest score this session: {high_score}")
    print("\nWould you like to play again?")
    print("1. Yes, launch another expedition!")
    print("2. No, return to base")

    choice = get_player_choice(["1", "2"])

    if choice == "1":
        show_message("\nPreparing new expedition...")
        time.sleep(1)
        start_game()
    else:
        show_message("\nThank you for playing Space Explorer!")
        show_message("May your next adventure be stellar!")

# Launch the game
if __name__ == "__main__":
    start_game()
