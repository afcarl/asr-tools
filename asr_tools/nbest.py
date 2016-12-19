from io import StringIO

"""
Representation of n-best lists.
"""

class NBest(object):
    """Represents an n-best list of ASR hypotheses."""

    def __init__(self, sentences, id_=None):
        """Sentences and IDs are required."""
        assert(sentences is not None)
        assert(len(sentences) > 0)
        self.sentences = sentences
        self.id_ = id_

    def __str__(self):
        """Returns a string representation of the object."""
        print_str = StringIO()
        print_str.write('ID: {}\n'.format(self.id_))
        for i, s in enumerate(self.sentences):
            print_str.write('{:3d} {}\n'.format(i + 1, s))
        return print_str.getvalue()

    def crop(self, n):
        self.sentences = self.sentences[:n]
    
    def hyp(self):
        return self.sentences[0]

    def oracle_hyp(self, n=None):
        """Find and return the sentence with the lowest WER in the n-best list."""    
        sentences = self.sentences
        if n: sentences = sentences[:n]
        return min(sentences, key=lambda x: x.wer())

    def is_improveable(self):
        return self.oracle_hyp().eval_.wer() < self.hyp().eval_.wer()
    
    def rank(self, sentence):
        return self.sentences.index(sentence)
