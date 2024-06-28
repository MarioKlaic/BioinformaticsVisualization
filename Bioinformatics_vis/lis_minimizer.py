from collections import defaultdict
def convert_to_numeric(sequence):
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
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
    for i in range(k,k+w - 1):
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
    for i in range(n - effective_w + 1, n-k+1):
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
def find_matching_minimizers(seq1, seq2):
    # Step 1: Create a dictionary for the second sequence, with lists of positions
    minimizer_dict = {}
    for minimizer in seq2:
        value = tuple(minimizer[0])
        position = minimizer[1]
        if value not in minimizer_dict:
            minimizer_dict[value] = []
        minimizer_dict[value].append(position)
    
    # Step 2: Find matches
    matches = []
    for minimizer in seq1:
        value = tuple(minimizer[0])
        position1 = minimizer[1]
        if value in minimizer_dict:
            for position2 in minimizer_dict[value]:
                matches.append([list(value), position1, position2])
    
    # Step 3: Sort the matches by the positions from the first sequence
    matches.sort(key=lambda x: x[1])
    
    # Step 4: Return the sorted matches
    return matches

def extract_position2_sequence(matches):
    return [match[2] for match in matches]

def longest_increasing_subsequences(arr):
    if not arr:
        return [], []
    # Temporary arrays to store the ends of each pile
    piles = []
    # To keep track of all possible predecessors
    predecessors = defaultdict(list)
    # Indices of the elements in arr
    positions = [-1] * len(arr)
    # List to store the state at each step
    states = []

    for i, num in enumerate(arr):
        # Binary search to find the position of num in piles
        left, right = 0, len(piles)
        while left < right:
            mid = (left + right) // 2
            if piles[mid] < num:
                left = mid + 1
            else:
                right = mid

        if left < len(piles):
            piles[left] = num
        else:
            piles.append(num)

        positions[left] = i
        if left > 0:
            predecessors[i].extend([positions[left - 1]])
        else:
            predecessors[i].append(-1)

        # Capture the state
        states.append({
            'step': i,
            'num': num,
            'piles': piles.copy(),
            'positions': positions.copy(),
            'predecessors': {k: v.copy() for k, v in predecessors.items()}
        })

    # Reconstruct all LIS paths using backtracking
    def backtrack(index):
        if index == -1:
            return [[]]
        result = []
        for pred in predecessors[index]:
            for seq in backtrack(pred):
                result.append(seq + [arr[index]])
        return result

    all_lis = []
    for pos in positions:
        if pos != -1:
            all_lis.extend(backtrack(pos))


    # Filter LIS of the maximum length
    max_len = len(piles)
    longest_sequence = []
    for seq in all_lis:
        if len(seq) == max_len:
            longest_sequence = seq
            break
    
    # Return the longest sequences and the states
    return longest_sequence, states

def find_minimizers_by_position2(position2_sequence, matches):
    # Create a dictionary from matches for quick lookup
    position2_to_match = {match[2]: match for match in matches}
    
    # Retrieve the minimizers for the given position2 sequence
    minimizers = []
    for pos2 in position2_sequence:
        if pos2 in position2_to_match:
            minimizers.append(position2_to_match[pos2])
    
    return minimizers

