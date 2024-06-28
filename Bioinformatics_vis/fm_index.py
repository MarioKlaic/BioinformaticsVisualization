class FM_INDEX:
    """
    A class representing the FM Index of a string, allowing efficient 
    pattern matching and other operations. Precomputes necessary structures 
    for fast queries.
    
    Attributes:
        t (str): The original text.
        bw (str): The Burrows-Wheeler Transform of the original text.
        rankAll (dict): Cumulative count of characters up to each position in BWT.
        tots (dict): Total count of each character in BWT.
        first (dict): Map from characters to their range of cells in the first column.
    """
    def __init__(self, t):
        """
        Initialize the FM Index with the given text.
        
        Args:
            t (str): The text to create the index for.
        """
        self.t = t
        self.bw = self.bwt(t)
        self.rankAll, self.tots = self.rankAllBwt(self.bw)
        self.first = self.firstCol(self.tots)

    def suffixArray(self, s):
        """
        Given a string s, return its suffix array.
        
        Args:
            s (str): The string to create the suffix array for.
            
        Returns:
            list: The suffix array of the string.
        """
        satups = sorted([(s[i:], i) for i in range(0, len(s) + 1)])
        return map(lambda x: x[1], satups)

    def bwt(self, t):
        """
        Given a string t, return its Burrows-Wheeler Transform.
        
        Args:
            t (str): The string to transform.
            
        Returns:
            str: The BWT of the string.
        """
        bw = []
        for si in self.suffixArray(t):
            if si == 0:
                bw.append('$')
            else:
                bw.append(t[si - 1])
        return ''.join(bw)

    def rankAllBwt(self, bw):
        """
        Calculate the rank of all characters in the BWT string.
        
        Args:
            bw (str): The BWT string.
            
        Returns:
            tuple: A map of lists with cumulative counts and total counts.
        """
        tots = {}
        rankAll = {}
        for c in bw:
            if c not in tots:
                tots[c] = 0
                rankAll[c] = []
        for c in bw:
            tots[c] += 1
            for ci in tots.keys():
                rankAll[ci].append(tots[ci])
        return rankAll, tots

    def firstCol(self, tots):
        """
        Calculate the range of cells in the first column for each character.
        
        Args:
            tots (dict): A dictionary with the total counts of each character.
            
        Returns:
            dict: A map from characters to their range of cells in the first column.
        """
        first = {}
        totc = 0
        for c, count in sorted(tots.items()):
            first[c] = (totc, totc + count)
            totc += count
        return first

    def reverseBwt(self, bw):
        """
        Reconstruct the original string from its BWT.
        
        Args:
            bw (str): The BWT string.
            
        Returns:
            str: The original string before the BWT.
        """
        ranks, tots = self.rankBwt(bw)
        first = self.firstCol(tots)
        rowi = 0
        t = '$'
        while bw[rowi] != '$':
            c = bw[rowi]
            t = c + t
            rowi = first[c][0] + ranks[rowi]
        return t

    def countMatches2(self, p):
        """
        Count the number of occurrences of a pattern in the text using the FM Index.
        
        Args:
            p (str): The pattern to match.
            
        Returns:
            int: The number of times the pattern occurs in the text.
        """
        if p[-1] not in self.first:
            return 0  # character doesn’t occur in T
        l, r = self.first[p[-1]]
        i = len(p) - 2
        while i >= 0 and r > l:
            c = p[i]
            l = self.first[c][0] + self.rankAll[c][l - 1]
            r = self.first[c][0] + self.rankAll[c][r - 1]
            i -= 1
        return r - l  # return size of final range

    def bwtMatrix(self):
        """
        Construct and return the entire BWT matrix for the text.
        
        Returns:
            list of str: A list where each element is a rotated string of the text.
        """
        t_with_dollar = self.t + '$'
        rotations = [t_with_dollar[i:] + t_with_dollar[:i] for i in range(len(t_with_dollar))]
        sorted_rotations = sorted(rotations)
        
        return sorted_rotations

