import FileParser as fp
from sklearn.externals import joblib
from sklearn import svm

parsers = [fp.FileParserIPRI(), fp.FileParserBulletinEconomical(), fp.FileParserVisnykGeo()]

training_vectors = []
training_output = []

for parser in parsers:
    parser.init_data()
    parser.read_data_training()
    training_vectors += parser.training_vectors
    training_output += parser.training_output

clf = svm.SVC()
clf.probability = True
clf.C = 1000
clf.fit(training_vectors, training_output)

joblib.dump(clf, 'svm.pkl')
