from sklearn.externals import joblib
import FileParser as fp
import VectorFilter as vf

clf = joblib.load('svm.pkl')
# vector = vf.VectorFilter()
# vector.parse_row('Occultation, Moon<br/>')
# print(vector.to_array())
# print(clf.predict([vector.to_array()]))
parsers = [("ipri", fp.FileParserIPRI()), ("iasa", fp.FileParserIASA()), ("infotelesc", fp.FileParserInfotelesc()),
           ("bulletin-economical", fp.FileParserBulletinEconomical()), ("visnyk-soc", fp.FileParserVisnykSoc()),
           ("scholar-publish", fp.FileParserScholarPublish()), ("imed-pub", fp.FileParserImedPub())]
for name, parser in parsers:
    parser.read_data_test()
    errors = parser.count_error(clf)
    print("Site {}".format(name))
    print("Common error {}%".format(errors[0]))
    print("Incorrect approved {}%".format(errors[1]))
    print("Incorrect blocked {}%".format(errors[2]))
    print("")
    parser.output_test_files()
