import string
def convert_to_numeric(sequence):

    start_index = 0

    # Initialize the mapping dictionary
    mapping = {}

    # Map uppercase letters A-Z
    for i, char in enumerate(string.ascii_uppercase, start=start_index):
        mapping[char] = i

    # Map lowercase letters a-z
    for i, char in enumerate(string.ascii_lowercase, start=start_index + 26):
        mapping[char] = i

    # Map special characters
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    for i, char in enumerate(special_characters, start=start_index + 52):
        mapping[char] = i
    return [mapping[char] for char in sequence]

def find_minimizers(sequence, k, w):
    def get_kmers(window, k):
        return [[window[i:i + k], i+1] for i in range(len(window) - k + 1)]

    # Convert sequence to numeric
    numeric_sequence = convert_to_numeric(sequence)
    n = len(numeric_sequence)
    
    minimizers = []
    
    # Calculate the effective window size
    effective_w = w + k - 1
    
    # Edge minimizers at the beginning
    for i in range(k, k + w - 1):
        window = numeric_sequence[:i]
        kmers = get_kmers(window, k)
        if kmers:  # Ensure there are k-mers in the window
            min_kmer = min(kmers)
            minimizers.append(min_kmer)
    
    # Main loop to find minimizers within window size effective_w
    for i in range(n - effective_w + 1):
        window = numeric_sequence[i:i + effective_w]
        kmers = get_kmers(window, k)
        min_kmer = min(kmers)
        min_kmer[1] += i
        minimizers.append(min_kmer)
    
    # Edge minimizers at the end
    for i in range(n - effective_w + 1, n - k + 1):
        window = numeric_sequence[i:]
        kmers = get_kmers(window, k)
        if kmers:  # Ensure there are k-mers in the window
            min_kmer = min(kmers)
            min_kmer[1] += i
            minimizers.append(min_kmer)
    
    return minimizers

def keep_unique_first_values(input_list):
    unique_entries = []
    for item in input_list:
        if item not in unique_entries:
            unique_entries.append(item)
    
    return unique_entries

def lcs_table(X, Y):
    m = len(X)
    n = len(Y)
    # Initialize the table with zeros
    table = [[0] * (n + 1) for _ in range(m + 1)]
    arrows = [[''] * (n + 1) for _ in range(m + 1)]
    
    # Fill the table according to the LCS algorithm
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1][0] == Y[j - 1][0]:  # Compare minimizers
                table[i][j] = table[i - 1][j - 1] + 1
                arrows[i][j] = 'diag'
            else:
                if table[i - 1][j] >= table[i][j - 1]:
                    table[i][j] = table[i - 1][j]
                    arrows[i][j] = 'up'
                else:
                    table[i][j] = table[i][j - 1]
                    arrows[i][j] = 'left'
    
    return table, arrows

def find_optimal_path(arrows):
    i, j = len(arrows) - 1, len(arrows[0]) - 1
    path = []

    while i > 0 or j > 0:
        path.append((i, j))
        if arrows[i][j] == 'diag':
            i -= 1
            j -= 1
        elif arrows[i][j] == 'up':
            i -= 1
        elif arrows[i][j] == 'left':
            j -= 1
        elif i > 0 and j == 0:
            i -= 1
        elif i == 0 and j > 0:
            j -= 1
        else:
            break

    path.append((i, j))
    path.reverse()
    return path
