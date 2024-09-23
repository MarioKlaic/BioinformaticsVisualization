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

def convert_to_characters(numeric_sequence):
    start_index = 0

    # Initialize the mapping dictionary
    reverse_mapping = {}

    # Reverse map uppercase letters A-Z
    for i, char in enumerate(string.ascii_uppercase, start=start_index):
        reverse_mapping[i] = char

    # Reverse map lowercase letters a-z
    for i, char in enumerate(string.ascii_lowercase, start=start_index + 26):
        reverse_mapping[i] = char

    # Reverse map special characters
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    for i, char in enumerate(special_characters, start=start_index + 52):
        reverse_mapping[i] = char

    # Convert numeric sequence to characters
    return ''.join([reverse_mapping[num] for num in numeric_sequence])

def find_minimizers(sequence, k, w):
    rows = []
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
        rows.append([k for k in range(i)])
        kmers = get_kmers(window, k)
        if kmers:  # Ensure there are k-mers in the window
            min_kmer = min(kmers)
            minimizers.append(min_kmer)
    
    # Main loop to find minimizers within window size effective_w
    for i in range(n - effective_w + 1):
        window = numeric_sequence[i:i + effective_w]
        rows.append([k for k in range(i, i + effective_w)])
        kmers = get_kmers(window, k)
        min_kmer = min(kmers)
        min_kmer[1] += i
        minimizers.append(min_kmer)
    
    # Edge minimizers at the end
    for i in range(n - effective_w + 1, n - k + 1):
        window = numeric_sequence[i:]
        rows.append([k for k in range(i,len(numeric_sequence))])
        kmers = get_kmers(window, k)
        if kmers:  # Ensure there are k-mers in the window
            min_kmer = min(kmers)
            min_kmer[1] += i
            minimizers.append(min_kmer)
    return minimizers, rows

def keep_unique_first_values(input_list):
    unique_entries = []
    for item in input_list:
        if item not in unique_entries:
            unique_entries.append(item)
    
    return unique_entries