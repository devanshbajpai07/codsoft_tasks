import random
import string

def get_character_set(complexity):
    """Return character set based on complexity level."""
    sets = {
        1: string.ascii_lowercase,
        2: string.ascii_lowercase + string.ascii_uppercase,
        3: string.ascii_lowercase + string.ascii_uppercase + string.digits,
        4: string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    }
    return sets.get(complexity, sets[4])
def generate_password(length, complexity):
    """Generate a random password with specified length and complexity."""
    chars = get_character_set(complexity)
    
    if complexity == 4:
        # Ensure at least one character from each category for highest complexity
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
        ]
        
        # Fill remaining positions with random characters
        for _ in range(length - 4):
            password.append(random.choice(chars))
            
        # Shuffle to avoid predictable pattern
        random.shuffle(password)
        return ''.join(password)
    else:
        return ''.join(random.choice(chars) for _ in range(length))

def display_complexity_options():
    """Display available complexity levels."""
    print("\nPassword Complexity Levels:")
    print("1. Lowercase letters only (a-z)")
    print("2. Mixed case letters (a-z, A-Z)")
    print("3. Letters and numbers (a-z, A-Z, 0-9)")
    print("4. Full complexity (letters, numbers, symbols)")

def main():
    """Main function to run the password generator."""
    print("=" * 50)
    print("         SECURE PASSWORD GENERATOR")
    print("=" * 50)
    
    while True:
        try:
            # Get password length
            length = int(input("\nEnter desired password length (4-128): "))
            
            if length < 4:
                print("Password length must be at least 4 characters for security.")
                continue
            elif length > 128:
                print("Password length cannot exceed 128 characters.")
                continue
                
            # Display complexity options
            display_complexity_options()
            
            # Get complexity level
            complexity = int(input("\nChoose complexity level (1-4): "))
            
            if complexity not in [1, 2, 3, 4]:
                print("Please choose a valid complexity level (1-4).")
                continue
            
            # Adjust length for full complexity if needed
            if complexity == 4 and length < 4:
                print("Full complexity requires minimum 4 characters.")
                continue
                
            # Generate password
            password = generate_password(length, complexity)
            
            # Display results
            print("\n" + "=" * 50)
            print("GENERATED PASSWORD:")
            print("=" * 50)
            print(f"Password: {password}")
            print(f"Length: {len(password)} characters")
            print(f"Complexity: Level {complexity}")
            print("=" * 50)
            
            # Ask if user wants another password
            again = input("\nGenerate another password? (y/n): ").lower()
            if again not in ['y', 'yes']:
                break
                
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
    
    print("\nThank you for using the Password Generator!")

if __name__ == "__main__":
    main()