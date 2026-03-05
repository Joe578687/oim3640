import random

def spelling_bee_game():
    """A simple spelling bee game where the user spells words correctly."""
    
    words = [
        "python", "programming", "algorithm", "database", "function",
        "variable", "iteration", "recursion", "exception", "dictionary"
    ]
    
    score = 0
    total = 5
    
    print("Welcome to the Spelling Bee Game!")S
    print(f"You will be asked to spell {total} words correctly.\n")
    
    for i in range(total):
        word = random.choice(words)
        print(f"Word {i + 1}: {word}")
        user_input = input("Spell the word: ").strip().lower()
        
        if user_input == word:
            print("✓ Correct!\n")
            score += 1
        else:
            print(f"✗ Wrong! The correct spelling is: {word}\n")
    
    print(f"Game Over! Your score: {score}/{total}")
    percentage = (score / total) * 100
    print(f"Percentage: {percentage:.1f}%")

if __name__ == "__main__":
    spelling_bee_game()