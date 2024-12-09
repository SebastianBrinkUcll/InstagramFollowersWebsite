import json
import os

def load_instagram_data(file_path):

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            usernames = set()
            
            # Handle different JSON structures
            if isinstance(data, dict):
                # Check for known keys
                if 'relationships_followers' in data:
                    entries = data['relationships_followers']
                elif 'relationships_following' in data:
                    entries = data['relationships_following']
                else:
                    print(f"No known keys found in {file_path}")
                    return set()
            elif isinstance(data, list):
                entries = data
            else:
                print(f"Unexpected data type in {file_path}")
                return set()
            
            # Extract usernames
            for entry in entries:
                if isinstance(entry, dict):
                    # Try different ways to extract username
                    if 'string_list_data' in entry and entry['string_list_data']:
                        username = entry['string_list_data'][0].get('value')
                        if username:
                            usernames.add(username)
                    elif 'value' in entry:
                        usernames.add(entry['value'])
                elif isinstance(entry, str):
                    usernames.add(entry)
            
            print(f"Extracted {len(usernames)} users from {os.path.basename(file_path)}")
            return usernames
            
    except Exception as e:
        print(f"DETAILED ERROR reading file {file_path}: {e}")
        return set()

def find_unfollowers(followers_file, following_file):
    """
    Find users you follow who do not follow you back.
    """
    # Load followers and following data
    followers = load_instagram_data(followers_file)
    following = load_instagram_data(following_file)
    
    # Find users you follow who do NOT follow you back
    unfollowers = following - followers
    
    print("\n=== Users You Follow Who Do Not Follow You Back ===")
    print(f"Total Unfollowers: {len(unfollowers)}")
    print("\nUnfollowers:")
    for username in sorted(unfollowers):
        print(username)
    
    # Save unfollowers to a text file
    output_file = os.path.join(os.path.dirname(following_file), 'unfollowers.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for username in sorted(unfollowers):
            f.write(f"{username}\n")
    print(f"\nUnfollowers list saved to {output_file}")
    
    return unfollowers

# Base path to your Instagram export
base_path = r"C:\Users\sebbr\side_projects\instagram_followers_project\instagram-seb.brink-2024-12-08-I1gI3EMz\connections\followers_and_following"

# Specific files
followers_file = os.path.join(base_path, 'followers_1.json')
following_file = os.path.join(base_path, 'following.json')

# Find and display unfollowers
find_unfollowers(followers_file, following_file)
