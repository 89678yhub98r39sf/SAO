
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from random import shuffle, choice, choices
from string import punctuation
from copy import deepcopy

#-------------------------------------------
#-------------------------------------------
"""
('diaphysis relating bone sulfa medicine like drug used also sulfadiazine veterinary putting interpretation wrong diaphysis relating bone good disconnected consisting small parts good putting interpretation wrong diaphysis relating bone diaphysis relating bone good putting interpretation wrong disconnected consisting small parts sulfa medicine like drug used also sulfadiazine veterinary sulfa medicine like drug used also sulfadiazine veterinary good good disconnected consisting small parts putting interpretation wrong disconnected consisting small parts sulfa medicine like drug used also sulfadiazine veterinary diaphysis relating bone disconnected consisting small parts disconnected consisting small parts good sulfa medicine like drug used also sulfadiazine veterinary diaphysis relating bone', 'dress garishly tastelessly leaf three shape lobes divided work caring sick injured infirm clearly able act intelligently mentally think confused clearly able act intelligently mentally think confused dress garishly tastelessly dress garishly tastelessly dress garishly tastelessly leaf three shape lobes divided dress garishly tastelessly work caring sick injured infirm work caring sick injured infirm clearly able act intelligently mentally think confused leaf three shape lobes divided clearly able act intelligently mentally think confused dress garishly tastelessly work caring sick injured infirm pays gaming table bets collects someone work caring sick injured infirm dress garishly tastelessly clearly able act intelligently mentally think confused')
"""
#-------------------------------------------

## problem : encoding a bag-of-words
"""
popular approach is to use frequency measures (tf-idf for example)
but since these are just bag-of-words, then have to find a way to `extract their meaning` first.

`Tree-Algorithm`
Take the following approach:
- for each word w, get d = definition(w).
- descriptorForWord = {d.split()}
- for each relevant word r in definition, get that definition d1.
- loop above steps until minimum number of descriptors is obtained for each Language
"""
#

# NOTE : TODO
"""
function
<fetch_nonstop_words>
is used in a try-except.
should be better.
"""
###
'''
could add a `fetchByTopics` variable
'''
class LanguageMaker:

    def __init__(self, topics = None):
        self.topics = topics

    '''
    description:
    - fetches nonstop words from NLTK corpus of size n

    arguments:
    - n := int
    - byTopic := bool

    return:
    - set(str)
    '''
    @staticmethod
    def fetch_nonstop_words(n, byTopic = False):

        if byTopic: raise NotImplementedError("fetching words by topic has not yet been implemented")

        """
        description:
        - performs random shuffling of words and returns x of them

        arguments:
        - x := int

        return:
        - set(str)
        """
        def fetch_words(x):
            q = words.words()
            shuffle(q)
            return set(q[:n])

        """
        description:
        - filters words that have empty synsets

        arguments:
        - words, set(str)

        return:
        - set(str)
        """
        def filter_irrelevant(words):
            newWords = set()
            for w in words:
                q = wn.synsets(w)
                if len(q) != 0: newWords |= {w}
            return newWords

        #$
        r = filter_irrelevant(LanguageMaker.filter_nonstop_words(fetch_words(n)))
        while True:
            diff = n - len(r)
            if diff == 0: break
            r_ = filter_irrelevant(LanguageMaker.filter_nonstop_words(fetch_words(diff * 300)))
            diff2 = len(r_) - diff
            if diff2 > 0:
                r_ = set(list(r_)[:diff])
            r |= r_
        return r

    @staticmethod
    def filter_nonstop_words(allWords):
        return {w for w in allWords if w not in stopwords.words("english")}

    '''
    description:
    - runs scikit-learn's k-means algorithm on the encodings of bagOfWords' definitions.
    '''
    def cluster_words_by_definition(self, bagOfWords, numClusters):
        return -1

    '''
    description:
    - gets descriptors for set of words into a dictionary
    '''
    @staticmethod
    def get_descriptors(wordSet, output):
        dk = None
        if output is dict:
            dk = {}
            for w in wordSet:
                dk[w] = LanguageMaker.get_descriptors_for_word(w)
        elif output is list:
            dk = []
            for w in wordSet:
                dk.extend(list(LanguageMaker.get_descriptors_for_word(w)))
        elif output is set:
            dk = set()
            for w in wordSet:
                dk |= LanguageMaker.get_descriptors_for_word(w)
        else:
            raise ValueError("some value errors here. for output : {}".format(output))

        return dk

    '''
    description:
    - gets the descriptors for the words.

    arguments:
    - word := str
    - minDescriptors := int
    '''
    @staticmethod
    def get_descriptors_for_word(word):
        try:
            q = wn.synsets(word)[0]
        except:
            return False
        lq = q.definition()
        exclude = set(punctuation) - {" "}
        lq = ''.join(ch for ch in lq if ch not in exclude)
        lq = lq.split(" ")
        defQ =  LanguageMaker.filter_nonstop_words(lq)
        return defQ

    '''
    description:
    -

    arguments:
    - minDescriptors :=
    - mode := geq | const
    '''
    @staticmethod
    def get_list_of_descriptors(minDescriptors, startSize, mode = "geq"):
        # get initial bag of descriptors
        x = list(LanguageMaker.fetch_nonstop_words(startSize))
        f_ = deepcopy(x)
        f = []
        while True:
            c = choice(x)
            f.extend(list(LanguageMaker.get_descriptors_for_word(c)))
            if len(f) >= minDescriptors: break
        return f_, f

    '''
    description:
    -

    arguments:
    - numLanguages := int
    - minSizeInfo := int | list(for each lang.)
    - startSizeInfo := int
    - mode := geq

    return:
    -
    '''
    @staticmethod
    def get_languages(numLanguages, minSizeInfo = 100, startSizeInfo = 5, mode = "geq"):

        '''
        return:
        - int, int
        '''
        def get_appropriate_values(index):
            if type(minSizeInfo) is int: ms = minSizeInfo
            else: ms = minSizeInfo[index]

            if type(startSizeInfo) is int: ss = startSizeInfo
            else: ss = startSizeInfo[index]
            return ms, ss

        languages = []
        for i in range(numLanguages):
            ms, ss = get_appropriate_values(i)
            ld = LanguageMaker.get_list_of_descriptors(ms, ss, mode)
            languages.append(ld)
        return languages

    """
    description:
    - given a list of centroids, gets their descriptors.

    arguments:
    - centroidsForEach :=
    - output := list | set

    return:
    - list | set
    """
    @staticmethod
    def get_languages_by_content(centroidsForEach, outputForEach = "list"):
        assert outputForEach in {list, set}, "invalid output : {}".format(output)
        dk = []
        for x in centroidsForEach:
            dk_ = LanguageMaker.get_descriptors(x, output = outputForEach)
            dk.append((x, dk_))
        return dk

    #!!
    def get_descriptors_for_bag_try_except(self, bagOfWords, minDescriptors, mode = "geq"):
        try:
            return self.get_descriptors_for_bag(bagOfWords, minDescriptors, mode)
        except:
            pass

    """
    description:
    -

    arguments:
    - b :=

    return:
    -
    """
    @staticmethod
    def get_descriptors_for_list(b):
        allDesc = []
        for l in b:
            d = LanguageMaker.get_descriptors_for_word(l)
            allDesc += list(d)
        return allDesc

    """
    description:
    - gets the descriptors for the words in the `Tree-Algorithm` described above

    arguments:
    - bagOfWords := set(str)
    - minDescriptors := int
    - mode := geq | const, geq outputs a descriptor set of minimum size `minDescriptors`
                       const outputs a descriptor set of constant size `minDescriptors`

    return:
    - set(str)
    """
    def get_descriptors_for_bag(self, bagOfWords, minDescriptors, mode = "geq"):
        assert mode in {"geq", "const"}, "invalid mode {}".format(mode)

        """
        description:
        - chooses appropriate number of random descriptors from set

        arguments:
        - ds := set(str), descriptor set
        - cd := set(str), collected descriptors
        - numWords := int

        return:
        - set(str), random words
        - set(str), collected descriptors
        """
        def choose_random_words(ds, cd, numWords:int = 10):
            x = set()
            termination = 100
            setTerm = False
            while len(x) < numWords:
                rw = set(choices(list(ds), k = numWords))
                rw -= cd
                if len(rw) == 0: break
                x |= rw
                cd |= rw
            return x, cd

        """
        description:
        ~

        arguments:
        - ds := set(str), descriptor set
        - maxL := int

        return:
        - set(str)
        """
        def get_descriptors_for_bag_of_words_(ds, maxL = None):
            # get initial descriptors for bagOfWords
            additionalDescriptors = set()
            n = 0
            for b in ds:
                d = self.get_descriptors_for_word(b)
                if d is False: break
                additionalDescriptors |= d
                n += len(d)
                if maxL != None:
                    if n >= maxL:
                        break
            if maxL != None:
                return set(list(additionalDescriptors)[:maxL])
            return additionalDescriptors

        numUniqueDescriptors = 0
        descriptorSet = set() # dict. : word -> descriptor
        collectedDescriptors = set() # already ran
        descriptorSet = get_descriptors_for_bag_of_words_(bagOfWords, minDescriptors if mode == "const" else None)

        # for required remaining descriptors, run above
        while True:
            x = len(descriptorSet) - minDescriptors
            if x >= 0: break
            q, collectedDescriptors = choose_random_words(descriptorSet, collectedDescriptors, 5)
            desc = get_descriptors_for_bag_of_words_(q, -x)
            descriptorSet |= desc
        return descriptorSet

'''
description:
- checks the size of descriptors of bag for minimum size requirement
'''
def LanguageMaker_GetDescriptorsForBag_Helper():
    x = LanguageMaker()
    bow = x.fetch_nonstop_words(100)
    desc = x.get_descriptors_for_bag(bow, 100)
    if desc is None:
        print("desk is None")
    assert len(desc) >= 100, "desc is len {}, want at least 100".format(len(desc))

    bow = x.fetch_nonstop_words(100)
    desc = x.get_descriptors_for_bag_try_except(bow, 100, "const")
    if desc is None:
        print("desk is None")
    assert len(desc) == 100, "desc is len {}, want exactly 100".format(len(desc))

def LanguageMaker_GetDescriptorsForBag_GoodCodeTest():
    for i in range(100):
        print("{}".format(i))
        LanguageMaker_GetDescriptorsForBag_Helper()

def LanguageMaker_GetDescriptorsForBag_ContentsTest():
    x = LanguageMaker()
    bow = x.fetch_nonstop_words(1)
    bow = {"* metamorphoses"}
    print("* word to look at :\n{}".format(bow))
    desc = x.get_descriptors_for_bag(bow, 100)
    print("* descriptors :\n")
    print(desc)

def LanguageMaker_GetDescriptorsForBag_ContentsTest():
    return LanguageMaker.get_list_of_descriptors(100, 5, mode = "geq")

def LanguageMaker_GetLanguages():
    return LanguageMaker.get_languages(5, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")

def LanguageMaker_GetLanguagesByContentSamples():
    centroidsForEach = [{"dog", "whale"}, {"cat", "rhino"}, {"water"}, {"hydrogen"}]
    return LanguageMaker.get_languages_by_content(centroidsForEach, outputForEach = list)


#----
x = LanguageMaker.get_descriptors_for_word("flower")
x2 =  LanguageMaker.get_descriptors_for_word("blossom")
#----