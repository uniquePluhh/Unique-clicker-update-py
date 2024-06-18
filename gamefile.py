import os
import subprocess
import requests
import random

# Function to check if running as admin (Windows)
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Function to request admin privileges (Windows)
def run_as_admin():
    if not is_admin():
        print("Requesting administrative privileges...")
        subprocess.run(["powershell.exe", "Start-Process", "python", "-Verb", "runAs"])
        exit()

# Function to update the script
def update_script(update_url, script_path):
    print("Checking for updates...")
    try:
        response = requests.get(update_url)
        if response.status_code == 200:
            with open(script_path, 'w') as f:
                f.write(response.text)
            print("Update downloaded successfully.")
            return True
        else:
            print(f"Failed to download the update. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to download the update: {str(e)}")
    return False

# Function to load game state
def load_game(save_file):
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            data = f.readlines()
            game_state = {}
            for line in data:
                key, value = line.strip().split('=')
                game_state[key.strip()] = int(value.strip())
            return game_state.get('clicks', 1000), game_state.get('cp', 1)
    return 1000, 1  # Default values if save file doesn't exist

# Function to save game state
def save_game(save_file, clicks, cp):
    with open(save_file, 'w') as f:
        f.write(f"clicks={clicks}\n")
        f.write(f"cp={cp}\n")

# Function to handle the game menu
def game_menu(clicks, cp):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(".                      ======================")
        print(".                          unique clicker")
        print(".                      ======================")
        print(f".                      Cp, {cp}")
        print(f".                      Clicks, {clicks}")
        print(".")
        print(".                      press 1 click")
        print(".                      press 2 shop")
        print(".                      press Q save and exit")
        print(".")
        print(".                      =======================")
        
        choice = input("Choose input: ").strip().lower()
        
        if choice == '1':
            clicks += cp
        elif choice == '2':
            clicks = shop(clicks, cp)
        elif choice == 'q':
            save_game(save_file, clicks, cp)
            print("Game saved. Exiting...")
            break
        else:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    exit()

# Function to handle the shop
def shop(clicks, cp):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(".                      ======================")
        print(".                      barrys shop of wonders")
        print(".                      ======================")
        print(f".                      Clicks, {clicks}")
        print(".")
        print(".                      1. 1 cp $35")
        print(".                      2. 2 cp $55")
        print(".                      3. 3 cp $85")
        print(".")
        print(".                      0. exit shop")
        print(".                      =======================")
        
        if random.randint(0, 1) == 1:
            special_offer_cp = random.randint(1, 99)
            special_offer_cost = random.randint(1, 9999)
            print(f".                      special offer +{special_offer_cp} cp for ${special_offer_cost}")
            print(".                      9. to buy special offer")
        
        choice = input("Choose input: ").strip()
        
        if choice == '1' and clicks >= 35:
            clicks -= 35
            cp += 1
        elif choice == '2' and clicks >= 55:
            clicks -= 55
            cp += 2
        elif choice == '3' and clicks >= 85:
            clicks -= 85
            cp += 3
        elif choice == '0':
            break
        elif choice == '9' and 'special_offer_cp' in locals() and 'special_offer_cost' in locals():
            if clicks >= special_offer_cost:
                clicks -= special_offer_cost
                cp += special_offer_cp
                del special_offer_cp, special_offer_cost
            else:
                print("Not enough clicks!")
        else:
            print("Invalid input or not enough clicks!")
        
        input("Press Enter to continue...")
    
    return clicks

if __name__ == "__main__":
    run_as_admin()
    
    save_file = os.path.join(os.environ.get('TEMP', '/tmp'), 'clicker_save.txt')
    update_flag = os.path.join(os.environ.get('TEMP', '/tmp'), 'clicker_update.flag')
    update_url = "https://raw.githubusercontent.com/uniquePluhh/Unique-clicker-update-py/main/gamefile.py"
    script_path = os.path.abspath(__file__)
    
    # Update the script
    if os.path.exists(update_flag):
        os.remove(update_flag)
    
    if update_script(update_url, script_path):
        print("Update applied. Restarting the script...")
        open(update_flag, 'a').close()
        subprocess.Popen(['python', __file__])
        exit()
    
    # Load game state
    clicks, cp = load_game(save_file)
    
    # Start game menu
    game_menu(clicks, cp)
