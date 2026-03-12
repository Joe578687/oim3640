import os
from collections import Counter
import re

def load_lyrics(data_folder="data"):
    """Load lyrics from singalongsong.txt in the data folder."""
    all_lyrics = ""

    if not os.path.exists(data_folder):
        print(f"Error: {data_folder} folder not found.")
        return all_lyrics

    filepath = os.path.join(data_folder, "singalongsong.txt")
    if not os.path.isfile(filepath):
        print(f"Error: {filepath} not found.")
        return all_lyrics

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            all_lyrics = file.read()
    except Exception as e:
        print(f"Error reading singalongsong.txt: {e}")

    return all_lyrics

def analyze_lyrics(lyrics, top_n=10):
    """Analyze lyrics and return most common words."""
    # Convert to lowercase and remove punctuation
    words = re.findall(r'\b[a-z]+\b', lyrics.lower())
    
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'was', 'are', 'be', 'been', 'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'of', 'it', 'you', 'i', 'me', 'my', 'we', 'he', 'she', 'that', 'this', 'your'}
    words = [word for word in words if word not in stop_words]
    
    # Count word frequency
    word_counts = Counter(words)
    
    return word_counts.most_common(top_n)

def main():
    """Main function to run the lyric analyzer."""
    print("=== Lyric Analyzer ===\n")
    
    lyrics = load_lyrics("data")
    
    if not lyrics.strip():
        print("No lyrics found. Ensure your 'data' folder contains .txt or .md files.")
        return
    
    top_words = analyze_lyrics(lyrics, top_n=15)
    
    print(f"Most frequently used words:\n")
    for i, (word, count) in enumerate(top_words, 1):
        print(f"{i}. '{word}' - {count} times")

if __name__ == "__main__":
    main()

print("Running from:", os.getcwd())