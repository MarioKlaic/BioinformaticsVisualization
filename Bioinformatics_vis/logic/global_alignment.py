class GlobalAlignment:

    def __init__(self):
        pass

    def needleman_wunsch(self, seq1, seq2, match=1, mismatch=-1, gap=-1):
        # Create the scoring matrix
        rows = len(seq1) + 1
        cols = len(seq2) + 1
        score_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        arrows = [['' for _ in range(cols)] for _ in range(rows)]  # Initialize arrows matrix

        # Initialize the first row and column
        for i in range(rows):
            score_matrix[i][0] = i * gap
        for j in range(cols):
            score_matrix[0][j] = j * gap

        # Fill the scoring matrix
        for i in range(1, rows):
            for j in range(1, cols):
                if seq1[i - 1] == seq2[j - 1]:
                    diagonal = score_matrix[i - 1][j - 1] + match
                else:
                    diagonal = score_matrix[i - 1][j - 1] + mismatch
                above = score_matrix[i - 1][j] + gap
                left = score_matrix[i][j - 1] + gap
                score_matrix[i][j] = max(diagonal, above, left)

                # Determine arrow direction
                if score_matrix[i][j] == diagonal:
                    arrows[i][j] += 'diag '  # Diagonal arrow
                if score_matrix[i][j] == above:
                    arrows[i][j] += 'up '  # Upward arrow
                if score_matrix[i][j] == left:
                    arrows[i][j] += 'left '  # Leftward arrow

        # Helper function to perform the traceback recursively
        def traceback(i, j, align1, align2, path):
            global sum_max
            if i == 0 and j == 0:
                path = [(i,j)] + path
                sum = 0
                for pair in path:
                    sum += score_matrix[pair[0]][pair[1]]
                if sum_max == None:
                    sum_max = sum
                    all_paths.append(path)
                    all_alignments.append((align1, align2))

                elif sum > sum_max:
                    sum_max = sum
                    all_paths.clear()
                    all_alignments.clear()
                    all_paths.append(path)
                    all_alignments.append((align1, align2))
                elif sum == sum_max:
                    all_paths.append(path)
                    all_alignments.append((align1, align2))
                return
            if 'diag' in arrows[i][j]:
                traceback(i - 1, j - 1, seq1[i - 1] + align1, seq2[j - 1] + align2, [(i, j)] + path)
            if 'up' in arrows[i][j]:
                traceback(i - 1, j, seq1[i - 1] + align1, '-' + align2, [(i, j)] + path)
            if 'left' in arrows[i][j]:
                traceback(i, j - 1, '-' + align1, seq2[j - 1] + align2, [(i, j)] + path)
            if 'diag' not in arrows[i][j] and 'up' not in arrows[i][j] and 'left' not in arrows[i][j]:
                if(i != 0):
                    traceback(i-1, j, seq1[i-1]+ align1, '-' + align2, [(i, j)] + path)
                if(j != 0):
                    traceback(i, j-1, '-' + align1, seq2[j-1] + align2, [(i, j)] + path)

        all_alignments = []
        all_paths = []
        global sum_max
        sum_max = None
        traceback(rows - 1, cols - 1, '', '', [])

        return all_alignments, all_paths, score_matrix[rows - 1][cols - 1], score_matrix, arrows
    
    def needleman_wunsch_semi_global(self, seq1, seq2, match=1, mismatch=-1, gap=-1):
        # Create the scoring matrix
        rows = len(seq1) + 1
        cols = len(seq2) + 1
        score_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        arrows = [['' for _ in range(cols)] for _ in range(rows)]  # Initialize arrows matrix

        # Initialize the first row and column to 0 (semi-global alignment initialization)
        for i in range(rows):
            score_matrix[i][0] = 0
        for j in range(cols):
            score_matrix[0][j] = 0

        # Fill the scoring matrix
        for i in range(1, rows):
            for j in range(1, cols):
                if seq1[i - 1] == seq2[j - 1]:
                    diagonal = score_matrix[i - 1][j - 1] + match
                else:
                    diagonal = score_matrix[i - 1][j - 1] + mismatch
                above = score_matrix[i - 1][j] + gap
                left = score_matrix[i][j - 1] + gap
                score_matrix[i][j] = max(diagonal, above, left)

                # Determine arrow direction
                if score_matrix[i][j] == diagonal:
                    arrows[i][j] += 'diag '  # Diagonal arrow
                if score_matrix[i][j] == above:
                    arrows[i][j] += 'up '  # Upward arrow
                if score_matrix[i][j] == left:
                    arrows[i][j] += 'left '  # Leftward arrow

        # Find the starting point for the traceback
        # We find the maximum score in the last row or last column
        max_score = -float('inf')
        start_pos_list = []

        # Check the last row
        for j in range(cols):
            if score_matrix[rows - 1][j] > max_score:
                max_score = score_matrix[rows - 1][j]
                start_pos_list.clear()   
                start_pos_list.append((rows - 1, j))
            elif score_matrix[rows - 1][j] == max_score:
                start_pos_list.append((rows - 1, j))

        # Check the last column
        for i in range(rows):
            if score_matrix[i][cols - 1] > max_score:
                max_score = score_matrix[i][cols - 1]
                start_pos_list.clear()
                start_pos_list.append((i, cols - 1))
            elif score_matrix[i][cols - 1] == max_score:
                start_pos_list.append((i, cols - 1))

        # Helper function to perform the traceback recursively
        def traceback(i, j, align1, align2, path):
            if i == 0 or j == 0:
                global sum_max
                path = [(i,j)] + path
                sum = 0
                for pair in path:
                    sum += score_matrix[pair[0]][pair[1]]
                if sum_max == None:
                    sum_max = sum
                    all_paths.append(path)
                    all_alignments.append((align1, align2))
                elif sum > sum_max:
                    sum_max = sum
                    all_paths.clear()
                    all_alignments.clear()
                    all_paths.append(path)
                    all_alignments.append((align1, align2))
                elif sum == sum_max:
                    if (align1, align2) not in all_alignments:
                        all_paths.append(path)
                        all_alignments.append((align1, align2))
                return
            if 'diag' in arrows[i][j]:
                traceback(i - 1, j - 1, seq1[i - 1] + align1, seq2[j - 1] + align2, [(i, j)] + path)
            if 'up' in arrows[i][j]:
                traceback(i - 1, j, seq1[i - 1] + align1, '-' + align2, [(i, j)] + path)
            if 'left' in arrows[i][j]:
                traceback(i, j - 1, '-' + align1, seq2[j - 1] + align2, [(i, j)] + path)

        all_alignments = []
        all_paths = []
        global sum_max
        sum_max = None
        for start_pos in start_pos_list:
            traceback(start_pos[0], start_pos[1], '', '', [])

        return all_alignments, all_paths, max_score, score_matrix, arrows
