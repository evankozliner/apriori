from helpers import *
from subprocess import call
from math import floor
import re

def stringify(doc):
    return reduce(lambda a,b: a + " " + b, doc)

def labelify(labels):
    return ["|" + label + "|" for label in labels]

def write_transactions_file(transactions):
    print "Writing transactions.txt file..."
    with open("transactions.txt", 'a+') as transactions_file:
        for transaction in transactions:
            transactions_file.write(stringify(transaction).encode("utf-8") + "\n")

def write_appearences_file(labels):
    # Create the labels file
    with open("appearences.txt", 'a+') as labels_file:
        labels_file.write("antecedent\n")
        for label in labels:
            labels_file.write(label + " consequent\n")

def extract_rule(line):
    antecedent_pattern = re.compile(r"^.*<- (.*) \(.*")
    antecedent = set(antecedent_pattern.match(line).group(1).split(" "))
    label = line.split("|")[1]
    return (antecedent, label)

def extract_support_and_confidence(line):
    support_and_conf_pattern = re.compile(r".*\((.*)\)")
    return map(float, support_and_conf_pattern.match(line).group(1).split(", "))

def parse_rule_file():
    print "Parsing rule-output.txt for classification rules..."
    rules, supports, confidences = [], [], []
    with open("rule-output.txt") as f:
        for line in f:
            rules.append(extract_rule(line))
            s, c = extract_support_and_confidence(line)
            supports.append(s)
            confidences.append(c)
    confidence_then_support = lambda r: (confidences[rules.index(r)], supports[rules.index(r)])
    return sorted(rules, key = confidence_then_support, reverse=True)

def get_most_common_label(labels):
    label_list = []
    for label_set in labels: label_list.extend(label_set)
    return max(set(label_list), key=label_list.count)

def predict_docs(docs):
    correct_count = 0
    default_count = 0
    rules = parse_rule_file()
    labels = [doc[0] for doc in docs]
    default_label = get_most_common_label(labels)

    print "Predicting test documents..."
    # Pick first rule that is a subset of each doc
    for doc in docs:
        prediction = predict_doc(rules,doc, default_label)
        if prediction == default_label: default_count += 1
        if prediction in doc[0]:
            correct_count += 1

    print str(float(default_count) / float(len(docs))) + " used default label"
    return str(float(correct_count) / float(len(docs)))

def predict_doc(rules, doc, default_label):
    prediction = None
    for rule in rules:
        if set(doc[1]) > set(rule[0]): 
            prediction = rule[1]
    if prediction == None: 
        prediction = default_label
    return prediction

def clean_docs(docs):
    print "Cleaning documents..."
    return [(doc[0], stem_doc(remove_stop_words_and_punc(doc[2])))
            for doc in docs if doc[2] is not '']

def main():
    docs = clean_docs(get_docs())
    
    # Use an 80 - 20 split
    num_docs = int(floor(len(docs) * .8))
    train_docs = docs[0:num_docs]
    test_docs = docs[num_docs:len(docs)]

    labels = set()
    for doc in docs: labels |= set(labelify(doc[0]))

    transactions = [set(doc[1] + labelify(doc[0])) for doc in train_docs]
    
    write_transactions_file(transactions)
    write_appearences_file(labels)

    call(['make', 'rules'])

    accuracy = predict_docs(test_docs)

if __name__ == "__main__":
    main()
