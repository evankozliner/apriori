import classifier as c 
from helpers import *
from subprocess import call
from math import floor

def main():
    docs = c.clean_docs(c.get_docs())
    num_docs = int(floor(len(docs) * .8))
    test_docs = docs[num_docs:len(docs)]

    hyperparameter_grid = []
    top_accuracy = (0,0)
    for support in range(5,38,3):
        hyperparameter_row = []
        for confidence in range(5,38,3):
            print "Running predictions with support: " + str(support) + \
                    " confidence: " + str(confidence)
            call(['./apriori_with_params.sh', str(support), str(confidence)])
            hyperparameter_row.append(c.predict_docs(test_docs))
        hyperparameter_grid.append(hyperparameter_row)
    print hyperparaemter_grid

if __name__ == "__main__":
    main()
