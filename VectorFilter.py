import re


class VectorFilter(object):

    def __init__(self):
        self.word_count = 0
        self.ratio_length = 0
        self.ratio_symbols = 0

    # Convert attributes to array format
    def to_array(self):
        vector = []
        for attr, value in sorted(self.__dict__.items()):
            vector.append(value)
        return vector

    def parse_row(self, row):
        # Get word count
        self.word_count = len(row.split())

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