from sklearn.externals import joblib
import FileParser as fp


clf = joblib.load('svm.pkl')
parsers = [("ipri", fp.FileParserIPRI()), ("iasa", fp.FileParserIASA())]
for name, parser in parsers:
    parser.read_data_test()
    errors = parser.count_error(clf)
    print("Site {}".format(name))
    print("Common error {}%".format(errors[0]))
    print("Incorrect approved {}%".format(errors[1]))
    print("Incorrect blocked {}%".format(errors[2]))
    print("")

