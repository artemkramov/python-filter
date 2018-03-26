import VectorFilter as vf
import codecs
import os
from os.path import isfile, join
import shutil
import glob
import re
import ntpath
import io


class FileParser:
    training_ratio = 0.8

    # Map number lines in training set to appropriate class
    training_mapper = []

    # Training vectors
    training_vectors = []

    # Training expected output for learning
    training_output = []

    # Files to estimate the learning error
    test_files = []

    path_all_files = ""

    path_training_files = ""

    path_test_files = ""

    path_output_test_files = ""

    # Read file and prepare vectors with expected output
    def _prepare_data(self, file, is_training):
        with codecs.open(file, 'r', encoding='utf8') as f:
            lines = f.readlines()
            test_file = TestFile()
            test_file.file_name = ntpath.basename(file)
            test_file.rows = []
            test_file.rows_output = []
            for number, line in enumerate(lines):
                if len(self._trim_html_tags(line)) == 0:
                    continue
                vector = vf.VectorFilter()
                vector.parse_row(self._trim_html_tags(line))
                if self.training_mapper[number] != -1:
                    self.training_output.append(self.training_mapper[number])
                    if is_training:
                        self.training_vectors.append(vector.to_array())
                    else:
                        test_item = TestItem()
                        test_item.vector = vector.to_array()
                        test_item.row = self._trim_html_tags(line)
                        test_file.rows.append(test_item)

        self.test_files.append(test_file)

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

    # Prepare training set from files
    def read_data_training(self):
        self.training_vectors = []
        self.training_output = []
        self._read_data(self.path_training_files, True)

    # Prepare test set to evaluate errors
    def read_data_test(self):
        self.test_files = []
        self.training_output = []
        self._read_data(self.path_test_files, False)

    # Count errors to make some estimation about method effectiveness
    def count_error(self, clf):
        incorrect_all = 0
        incorrect_approved = 0
        incorrect_blocked = 0
        errors = [0, 0, 0]
        length = 0

        # Loop through all test files
        for index_file, test_file in enumerate(self.test_files):

            # Loop all rows and predict the result using classifier model
            for index, test_item in enumerate(test_file.rows):
                prediction = clf.predict([test_item.vector])[0]

                # if expected result is -1 (can't be set definitely)
                # than skip it
                if self.training_output[index] != -1:
                    length += 1

                    # If expected result doesn't correspond to real
                    # than detect the error and increment error counters
                    # Else write appropriate results
                    if prediction != self.training_output[index]:
                        incorrect_all += 1
                        if self.training_output[index] == 1:
                            incorrect_blocked += 1
                        else:
                            incorrect_approved += 1
                if prediction == 1:
                    self.test_files[index_file].rows_output.append(test_item)

        # Count all errors
        errors[0] = self._format_error(incorrect_all, length)
        errors[1] = self._format_error(incorrect_approved, length)
        errors[2] = self._format_error(incorrect_blocked, length)

        return errors

    def output_test_files(self):
        self._clear_folder(self.path_output_test_files)
        for test_file in self.test_files:
            path = self.path_output_test_files + test_file.file_name
            file = io.open(path, "w", encoding="utf-8")
            for test_item in test_file.rows_output:
                file.write(test_item.row + "\n")
            file.close()

    @staticmethod
    def _format_error(incorrect_count, length):
        return round(100 * (incorrect_count / length), 2)

    @staticmethod
    def copy_files(files, source, destination):
        for file in files:
            shutil.copy(source + file, destination + file)

    @staticmethod
    def _clear_folder(folder):
        files = glob.glob(folder + "*.txt")
        for f in files:
            os.remove(f)

    @staticmethod
    def _trim_html_tags(line):
        substring = ""
        regex = '^<[^<]+?>$'
        line = line.rstrip('\r\n')
        for index in range(len(line)):
            substring += line[index]
            if re.match(regex, substring):
                index += 1
                line = line[index:]
                break
        substring = ""
        for index in range(len(line)):
            i = len(line) - index - 1
            substring += line[i]
            if re.match(regex, substring):
                line = line[i:]
                break

        return line


# Test item which corresponds to row and vector in file
class TestItem:

    vector = []
    row = ""


# Test file
class TestFile:

    file_name = ""
    rows = []
    rows_output = []


class FileParserIPRI(FileParser):
    training_mapper = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]

    path_all_files = "data\\ipri.kiev.ua\\output\\"

    path_training_files = "data\\ipri.kiev.ua\\training\\"

    path_test_files = "data\\ipri.kiev.ua\\test\\"

    path_output_test_files = "data\\ipri.kiev.ua\\output_test\\"


class FileParserIASA(FileParser):
    training_mapper = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]

    path_all_files = "data\\journal.iasa.kpi.ua\\output\\"

    path_training_files = "data\\journal.iasa.kpi.ua\\training\\"

    path_test_files = "data\\journal.iasa.kpi.ua\\test\\"

    path_output_test_files = "data\\journal.iasa.kpi.ua\\output_test\\"


class FileParserInfotelesc(FileParser):
    training_mapper = [0, 0, 0, 1, 1, 1, 0, -1, 0, -1, 0, 0]

    path_all_files = "data\\infotelesc.kpi.ua\\output\\"

    path_training_files = "data\\infotelesc.kpi.ua\\training\\"

    path_test_files = "data\\infotelesc.kpi.ua\\test\\"

    path_output_test_files = "data\\infotelesc.kpi.ua\\output_test\\"


class FileParserBulletinEconomical(FileParser):
    training_mapper = [0, 1, 1, 1, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0]

    path_all_files = "data\\bulletin-econom.univ.kiev.ua\\output\\"

    path_training_files = "data\\bulletin-econom.univ.kiev.ua\\training\\"

    path_test_files = "data\\bulletin-econom.univ.kiev.ua\\test\\"

    path_output_test_files = "data\\bulletin-econom.univ.kiev.ua\\output_test\\"


class FileParserVisnykGeo(FileParser):
    training_mapper = [0, 1, 1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0]

    path_all_files = "data\\visnyk-geo.univ.kiev.ua\\output\\"

    path_training_files = "data\\visnyk-geo.univ.kiev.ua\\training\\"

    path_test_files = "data\\visnyk-geo.univ.kiev.ua\\test\\"

    path_output_test_files = "data\\visnyk-geo.univ.kiev.ua\\output_test\\"


class FileParserScholarPublish(FileParser):
    training_mapper = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0]

    path_all_files = "data\\scholarpublishing.org\\output\\"

    path_training_files = "data\\scholarpublishing.org\\training\\"

    path_test_files = "data\\scholarpublishing.org\\test\\"

    path_output_test_files = "data\\scholarpublishing.org\\output_test\\"


class FileParserImedPub(FileParser):
    training_mapper = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    path_all_files = "data\\www.imedpub.com\\output\\"

    path_training_files = "data\\www.imedpub.com\\training\\"

    path_test_files = "data\\www.imedpub.com\\test\\"

    path_output_test_files = "data\\www.imedpub.com\\output_test\\"


class FileParserVisnykSoc(FileParser):
    training_mapper = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    path_all_files = "data\\visnyk.soc.univ.kiev.ua\\output\\"

    path_training_files = "data\\visnyk.soc.univ.kiev.ua\\training\\"

    path_test_files = "data\\visnyk.soc.univ.kiev.ua\\test\\"

    path_output_test_files = "data\\visnyk.soc.univ.kiev.ua\\output_test\\"


class FileParserAmcs(FileParser):
    training_mapper = [0, 0, 1, 1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    path_all_files = "data\\swww.amcs.uz.zgora.pl\\output\\"

    path_training_files = "data\\swww.amcs.uz.zgora.pl\\training\\"

    path_test_files = "data\\swww.amcs.uz.zgora.pl\\test\\"

    path_output_test_files = "data\\swww.amcs.uz.zgora.pl\\output_test\\"

