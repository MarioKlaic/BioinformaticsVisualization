class SAIS:
    def __init__(self):
        self.S_TYPE = ord("S")
        self.L_TYPE = ord("L")
        self.steps_dictionary = {}
        pass

    def buildTypeMap(self, data):
        """
        Builds a map marking each suffix of the data as S_TYPE or L_TYPE.
        """
        # The map should contain one more entry than there are characters
        # in the string, because we also need to store the type of the
        # empty suffix between the last character and the end of the
        # string.
        res = bytearray(len(data) + 1)
        
        # The empty suffix after the last character is S_TYPE
        res[-1] = self.S_TYPE
        
        # If this is an empty string...
        if not len(data):
            # ...there are no more characters, so we're done.
            return res
        
        # The suffix containing only the last character must necessarily
        # be larger than the empty suffix.
        res[-2] = self.L_TYPE
        
        # Step through the rest of the string from right to left.
        for i in range(len(data)-2, -1, -1):
            if data[i] > data[i+1]:
                res[i] = self.L_TYPE
            elif data[i] == data[i+1] and res[i+1] == self.L_TYPE:
                res[i] = self.L_TYPE
            else:
                res[i] = self.S_TYPE
        
        return res
    
    def buildTypeMapString(self, data):
        """
        helper function returning a jsonify-able result
        """
        res = list("0" *(len(data)+1))
        res[-1] = "S"
        if not len(data):
            return res
        
        res[-2] = "L"
        for i in range(len(data)-2, -1, -1):
            if data[i] > data[i+1]:
                res[i] = "L"
            elif data[i] == data[i+1] and res[i+1] == self.L_TYPE:
                res[i] = "L"
            else:
                res[i] = "S"
        
        return res

    def isLMSChar(self, offset, typemap):
        """
        Returns true if the character at offset is a left-most S-type.
        """
        if offset == 0:
            return False
        if typemap[offset] == self.S_TYPE and typemap[offset - 1] == self.L_TYPE:
            return True

        return False

    def showTypeMap(self, data):
        typemap = self.buildTypeMap(data)

        print(data.decode('ascii'))
        print(typemap.decode('ascii'))

        print("".join(
                "^" if self.isLMSChar(i, typemap) else " "
                for i in range(len(typemap))
            ))
        
    def lmsSubstringsAreEqual(self, string, typemap, offsetA, offsetB):
        """
        Return True if LMS substrings at offsetA and offsetB are equal.
        """
        # No other substring is equal to the empty suffix.
        if offsetA == len(string) or offsetB == len(string):
            return False

        i = 0
        while True:
            aIsLMS = self.isLMSChar(i + offsetA, typemap)
            bIsLMS = self.isLMSChar(i + offsetB, typemap)

            # If we've found the start of the next LMS substrings...
            if (i > 0 and aIsLMS and bIsLMS):
                # ...then we made it all the way through our original LMS
                # substrings without finding a difference, so we can go
                # home now.
                return True

            if aIsLMS != bIsLMS:
                # We found the end of one LMS substring before we reached
                # the end of the other.
                return False

            if string[i + offsetA] != string[i + offsetB]:
                # We found a character difference, we're done.
                return False

            i += 1

    def encode_string(self, input_string):
        input_string = input_string.decode('ascii')
        encoded_list = []
        for char in input_string.lower():
            if char.isalpha():
                encoded_list.append(ord(char) - ord('a'))
        return encoded_list

    def findBucketSizes(self, string, alphabetSize=256):
        res = [0] * alphabetSize

        for char in string:
            res[char] += 1

        return res

    def findBucketHeads(self, bucketSizes):
        offset = 1
        res = []
        for size in bucketSizes:
            res.append(offset)
            offset += size

        return res

    def findBucketTails(self, bucketSizes):
        offset = 1
        res = []
        for size in bucketSizes:
            offset += size
            res.append(offset - 1)

        return res

    def showSuffixArray(self, arr, pos=None, function_name = ""):
        l = len(self.steps_dictionary.keys())
        self.steps_dictionary[l] = (arr[:], pos, function_name)
        print(" ".join("%02d" % each for each in arr))

        if pos is not None:
            print(" ".join(
                    "^^" if each == pos else "  "
                    for each in range(len(arr))
            ))

    def guessLMSSort(self, string, bucketSizes, typemap):
        """
        Make a suffix array with LMS-substrings approximately right.
        """
        # Create a suffix array with room for a pointer to every suffix of
        # the string, including the empty suffix at the end.
        guessedSuffixArray = [-1] * (len(string) + 1)

        bucketTails = self.findBucketTails(bucketSizes)

        # Bucket-sort all the LMS suffixes into their appropriate bucket.
        for i in range(len(string)):
            if not self.isLMSChar(i, typemap):
                # Not the start of an LMS suffix
                continue

            # Which bucket does this suffix go into?
            bucketIndex = string[i]
            # Add the start position at the tail of the bucket...
            guessedSuffixArray[bucketTails[bucketIndex]] = i
            # ...and move the tail pointer down.
            bucketTails[bucketIndex] -= 1

            # Show the current state of the array
            self.showSuffixArray(guessedSuffixArray, function_name="guessSA")

        # The empty suffix is defined to be an LMS-substring, and we know
        # it goes at the front.
        guessedSuffixArray[0] = len(string)

        self.showSuffixArray(guessedSuffixArray, function_name="guessSA")

        return guessedSuffixArray

    def induceSortL(self, encoded_string, guessedSuffixArray, bucketSizes, typemap):
        """
        Slot L-type suffixes into place.
        """
        bucketHeads = self.findBucketHeads(bucketSizes)

        # For each cell in the suffix array....
        for i in range(len(guessedSuffixArray)):
            if guessedSuffixArray[i] == -1:
                # No offset is recorded here.
                continue

            # We're interested in the suffix that begins to the left of
            # the suffix this entry points at.
            j = guessedSuffixArray[i] - 1
            if j < 0:
                # This entry in the suffix array is the suffix that begins
                # at the start of the string, offset 0. Therefore there is
                # no suffix to the left of it, and j is out of bounds of
                # the typemap.
                continue
            if typemap[j] != self.L_TYPE:
                # We're only interested in L-type suffixes right now.
                continue

            # Which bucket does this suffix go into?
            
            bucketIndex = encoded_string[j]
            # Add the start position at the head of the bucket...
            guessedSuffixArray[bucketHeads[bucketIndex]] = j
            # ...and move the head pointer up.
            bucketHeads[bucketIndex] += 1

            self.showSuffixArray(guessedSuffixArray, i, function_name="induceSortL")
            
    def induceSortS(self, encoded_string, guessedSuffixArray, bucketSizes, typemap):
        """
        Slot S-type suffixes into place.
        """
        bucketTails = self.findBucketTails(bucketSizes)

        for i in range(len(guessedSuffixArray)-1, -1, -1):
            j = guessedSuffixArray[i] - 1
            if j < 0:
                # This entry in the suffix array is the suffix that begins
                # at the start of the string, offset 0. Therefore there is
                # no suffix to the left of it, and j is out of bounds of
                # the typemap.
                continue
            if typemap[j] != self.S_TYPE:
                # We're only interested in S-type suffixes right now.
                continue

            # Which bucket does this suffix go into?
            bucketIndex = encoded_string[j]
            # Add the start position at the tail of the bucket...
            guessedSuffixArray[bucketTails[bucketIndex]] = j
            # ...and move the tail pointer down.
            bucketTails[bucketIndex] -= 1

            self.showSuffixArray(guessedSuffixArray, i, function_name="induceSortS")
    def summariseSuffixArray(self, string, guessedSuffixArray, typemap):
        """
        Construct a 'summary string' of the positions of LMS-substrings.
        """
        # We will use this array to store the names of LMS substrings in
        # the positions they appear in the original string.
        lmsNames = [-1] * (len(string) + 1)

        # Keep track of what names we've allocated.
        currentName = 0

        # Where in the original string was the last LMS suffix we checked?
        lastLMSSuffixOffset = None

        # We know that the first LMS-substring we'll see will always be
        # the one representing the empty suffix, and it will always be at
        # position 0 of suffixOffset.
        lmsNames[guessedSuffixArray[0]] = currentName
        lastLMSSuffixOffset = guessedSuffixArray[0]
        self.showSuffixArray(lmsNames, function_name="summariseSuffixArray")

        # For each suffix in the suffix array...
        for i in range(1, len(guessedSuffixArray)):
            # ...where does this suffix appear in the original string?
            suffixOffset = guessedSuffixArray[i]

            # We only care about LMS suffixes.
            if not self.isLMSChar(suffixOffset, typemap):
                continue

            # If this LMS suffix starts with a different LMS substring
            # from the last suffix we looked at....
            if not self.lmsSubstringsAreEqual(string, typemap,
                    lastLMSSuffixOffset, suffixOffset):
                # ...then it gets a new name
                currentName += 1

            # Record the last LMS suffix we looked at.
            lastLMSSuffixOffset = suffixOffset

            # Store the name of this LMS suffix in lmsNames, in the same
            # place this suffix occurs in the original string.
            lmsNames[suffixOffset] = currentName
            self.showSuffixArray(lmsNames, function_name="summariseSuffixArray")

        # Now lmsNames contains all the characters of the suffix string in
        # the correct order, but it also contains a lot of unused indexes
        # we don't care about and which we want to remove. We also take
        # this opportunity to build summarySuffixOffsets, which tells
        # us which LMS-suffix each item in the summary string represents.
        # This will be important later.
        summarySuffixOffsets = []
        summaryString = []
        for index, name in enumerate(lmsNames):
            if name == -1:
                continue
            summarySuffixOffsets.append(index)
            summaryString.append(name)

        # The alphabetically smallest character in the summary string
        # is numbered zero, so the total number of characters in our
        # alphabet is one larger than the largest numbered character.
        summaryAlphabetSize = currentName + 1

        return summaryString, summaryAlphabetSize, summarySuffixOffsets

    def makeSummarySuffixArray(self, summaryString, summaryAlphabetSize):
        """
        Construct a sorted suffix array of the summary string.
        """
        if summaryAlphabetSize == len(summaryString):
            # Every character of this summary string appears once and only
            # once, so we can make the suffix array with a bucket sort.
            summarySuffixArray = [-1] * (len(summaryString) + 1)

            # Always include the empty suffix at the beginning.
            summarySuffixArray[0] = len(summaryString)

            for x in range(len(summaryString)):
                y = summaryString[x]
                summarySuffixArray[y+1] = x

        else:
            # This summary string is a little more complex, so we'll have
            # to use recursion.
            summarySuffixArray = self.makeSuffixArrayByInducedSorting(
                summaryString,
                summaryAlphabetSize,
                recursion=True
            )

        return summarySuffixArray

    def accurateLMSSort(self, string, bucketSizes, typemap,
            summarySuffixArray, summarySuffixOffsets):
        """
        Make a suffix array with LMS suffixes exactly right.
        """
        # A suffix for every character, plus the empty suffix.
        suffixOffsets = [-1] * (len(string) + 1)

        # As before, we'll be adding suffixes to the ends of their
        # respective buckets, so to keep them in the right order we'll
        # have to iterate through summarySuffixArray in reverse order.
        bucketTails = self.findBucketTails(bucketSizes)
        for i in range(len(summarySuffixArray)-1, 1, -1):
            stringIndex = summarySuffixOffsets[summarySuffixArray[i]]

            # Which bucket does this suffix go into?
            bucketIndex = string[stringIndex]
            # Add the suffix at the tail of the bucket...
            suffixOffsets[bucketTails[bucketIndex]] = stringIndex
            # ...and move the tail pointer down.
            bucketTails[bucketIndex] -= 1

            self.showSuffixArray(suffixOffsets, function_name="accurateLMSSort")

        # Always include the empty suffix at the beginning.
        suffixOffsets[0] = len(string)

        self.showSuffixArray(suffixOffsets, function_name="accurateLMSSort")

        return suffixOffsets

    def makeSuffixArrayByInducedSorting(self, string, alphabetSize, recursion = False):
        if not recursion:
            self.steps_dictionary = {}
        """
        Compute the suffix array of 'string' with the SA-IS algorithm.
        """

        # Classify each character of the string as S_TYPE or L_TYPE
        typemap = self.buildTypeMap(string)


        # We'll be slotting suffixes into buckets according to what
        # character they start with
        bucketSizes = self.findBucketSizes(string, alphabetSize)

        # Use a simple bucket-sort to insert all the LMS suffixes into
        # approximately the right place the suffix array.
        guessedSuffixArray = self.guessLMSSort(string, bucketSizes, typemap)

        # Slot all the other suffixes into guessedSuffixArray, by using
        # induced sorting. This may move the LMS suffixes around.
        self.induceSortL(string, guessedSuffixArray, bucketSizes, typemap)
        self.induceSortS(string, guessedSuffixArray, bucketSizes, typemap)

        # Create a new string that summarises the relative order of LMS
        # suffixes in the guessed suffix array.
        summaryString, summaryAlphabetSize, summarySuffixOffsets = \
            self.summariseSuffixArray(string, guessedSuffixArray, typemap)

        # Make a sorted suffix array of the summary string.
        summarySuffixArray = self.makeSummarySuffixArray(
            summaryString,
            summaryAlphabetSize,
        )

        # Using the suffix array of the summary string, determine exactly
        # where the LMS suffixes should go in our final array.
        result = self.accurateLMSSort(string, bucketSizes, typemap,
                summarySuffixArray, summarySuffixOffsets)

        # ...and once again, slot all the other suffixes into place with
        # induced sorting.
        self.induceSortL(string, result, bucketSizes, typemap)
        self.induceSortS(string, result, bucketSizes, typemap)

        return result
    
    def getSteps(self):
        return self.steps_dictionary