import re
import numpy


class VectorFilter(object):

    def __init__(self):
        self.avg_word_length = 0
        self.ratio_length = 0
        self.ratio_symbols = 0
        self.ratio_word_clear = 0

    # Convert attributes to array format
    def to_array(self):
        vector = []
        for attr, value in sorted(self.__dict__.items()):
            vector.append(value)
        return vector

    def parse_row(self, row):

        # Get HTML tag ratio
        pattern = r"<[\/a-zA-Z0-9]{1,}>"
        matches = re.findall(pattern, row)
        html_length = 0
        for match in matches:
            html_length += len(match)
        self.ratio_length = html_length / len(row)

        # Get non-alphanumerical ratio
        non_alphanumeric_length = re.sub('[a-zA-Z]+', '*', row).count('*')
        self.ratio_symbols = non_alphanumeric_length / len(row)

        words = row.split()
        words_length = []
        word_clear_count = 0
        for word in words:
            is_word_correct = False
            if re.match('^[a-zA-Z0-9.,]+$', word):
                word_clear_count += 1
            for i in word:
                if i.isalnum():
                    is_word_correct = True
                    break
            if is_word_correct:
                words_length.append(len(word))

        if len(words_length) > 0:
            self.avg_word_length = numpy.mean(words_length)

        self.ratio_word_clear = 1.0 * word_clear_count / len(words)