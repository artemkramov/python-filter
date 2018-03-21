import VectorFilter as vf
import codecs
import os
from os.path import isfile, join
import shutil
import glob


class FileParser:

    training_ratio = 0.7

    # Map number lines in training set to appropriate class
    training_mapper = []

    # Training vectors
    training_vectors = []

    # Training expected output for learning
    training_output = []

    # Vectors to estimate the learning error
    test_vectors = []

    path_all_files = ""

    path_training_files = ""

    path_test_files = ""

    # Read file and prepare vectors with expected output
    def _prepare_data(self, file, is_training):
        with codecs.open(file, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for number, line in enumerate(lines):
                vector = vf.VectorFilter()
                vector.parse_row(line)
                self.training_output.append(self.training_mapper[number])
                if is_training:
                    self.training_vectors.append(vector.to_array())
                else:
                    self.test_vectors.append(vector.to_array())

    # Read all files in directory and split them into test and training subsets
    def _read_data(self, folder, is_training):
        files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
        for file in files:
            file = folder + "\\" + file
            self._prepare_data(file, is_training)

    # Split all input files into training and test set
    def init_data(self):

        # Clear input folders
        self._clear_folder(self.path_training_files)
        self._clear_folder(self.path_test_files)

        # Get all files and split it by the given ratio
        files = [f for f in os.listdir(self.path_all_files) if isfile(join(self.path_all_files, f))]
        index = int(round(len(files) * self.training_ratio))
        training_files = files[:index]
        test_files = files[index:]

        # Copy exploded data to appropriate folders
        self.copy_files(training_files, self.path_all_files, self.path_training_files)
        self.copy_files(test_files, self.path_all_files, self.path_test_files)

    def read_data_training(self):
        self._read_data(self.path_training_files, True)

    def read_data_test(self):
        self._read_data(self.path_test_files, False)

    def count_error(self, clf):
        incorrect_all = 0
        incorrect_approved = 0
        incorrect_blocked = 0
        errors = [0, 0, 0]

        for index, vector in enumerate(self.test_vectors):
            if clf.predict([vector])[0] != self.training_output[index]:
                incorrect_all += 1
                if self.training_output[index] == 1:
                    incorrect_blocked += 1
                else:
                    incorrect_approved += 1
        errors[0] = self._format_error(incorrect_all)
        errors[1] = self._format_error(incorrect_approved)
        errors[2] = self._format_error(incorrect_blocked)

        return errors

    def _format_error(self, incorrect_count):
        return round(100 * (incorrect_count / len(self.test_vectors)), 2)

    @staticmethod
    def copy_files(files, source, destination):
        for file in files:
            shutil.copy(source + file, destination + file)

    @staticmethod
    def _clear_folder(folder):
        files = glob.glob(folder + "*.txt")
        for f in files:
            os.remove(f)


class FileParserIPRI(FileParser):

    training_mapper = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]

    path_all_files = "data\\ipri.kiev.ua\\output\\"

    path_training_files = "data\\ipri.kiev.ua\\training\\"

    path_test_files = "data\\ipri.kiev.ua\\test\\"


class FileParserIASA(FileParser):

    training_mapper = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]

    path_all_files = "data\\journal.iasa.kpi.ua\\output\\"

    path_training_files = "data\\journal.iasa.kpi.ua\\training\\"

    path_test_files = "data\\journal.iasa.kpi.ua\\test\\"
