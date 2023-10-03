import collections

def load_dictionary(dictionary_file):
    try:
        with open(dictionary_file, "r") as file:
            return set(line.strip().lower() for line in file)
    except FileNotFoundError:
        print(f"File '{dictionary_file}' not found.")
        return set()

def calculate_probability(word, dictionary):
    
    word_counts = collections.Counter(dictionary)
    total_words = len(dictionary)

    if word in word_counts:
        word_probability = word_counts[word] / total_words
    else:
        word_probability = 1 / (total_words * 10)

    return word_probability

def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]

def suggest_best_correction(word, dictionary):
    word = word.lower()
    
    if word in dictionary:
        return word  # Return the word itself if it's in the dictionary

    best_correction = None
    best_distance = float('inf')
    best_probability = 0.0
    
    for entry in dictionary:
        distance = edit_distance(word, entry)
        if distance <= 2:  # Calculate edit distance only for 1 and 2
            entry_probability = calculate_probability(entry, dictionary)
            if distance < best_distance or (distance == best_distance and entry_probability > best_probability):
                best_correction = entry
                best_distance = distance
                best_probability = entry_probability
    
    return best_correction

def tokenize_input(input_text):
    delimiters = [' ', '.', "'"]
    current_word = ''
    tokens = []

    for char in input_text:
        if char in delimiters:
            if current_word:
                tokens.append(current_word)
            current_word = ''
        else:
            current_word += char
    
    if current_word:
        tokens.append(current_word)
    
    return tokens


dictionary_file = "big.txt"  
dictionary = load_dictionary(dictionary_file)

if not dictionary:
  print("no file found")

print("Enter text for spell checking (type 'exit' to quit):")
    
while True:
    user_input = input("> ")
        
    if user_input == 'exit':
            break

    tokens = tokenize_input(user_input)
        
    if not tokens:
        print("No words found.")
    else:
        for token in tokens:
            best_correction = suggest_best_correction(token, dictionary)
            if best_correction:
                print(f"Best Correction for '{token}': {best_correction}")
            else:
                print(f"No suggestions found for '{token}'.")

