import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    data = ([],[])
    month = {
    "Jan": 0,
    "Feb": 1,
    "Mar": 2,
    "Apr": 3,
    "May": 4,
    "June": 5,
    "Jul": 6,
    "Aug": 7,
    "Sep": 8,
    "Oct": 9,
    "Nov": 10,
    "Dec": 11}
    # Opens the csv and add information to info list 
    with open(filename, newline='') as csvfile:
        user = csv.reader(csvfile,delimiter=',')
        next(user)
        for line in user:
            individual = []

            # Modifies evevery column before appending to data
            # Page type
            individual.append(int(line[0]))
            individual.append(float(line[1]))
            individual.append(int(line[2]))
            individual.append(float(line[3]))
            individual.append(int(line[4]))    
            individual.append(float(line[5]))

            # Google analytics data
            individual.append(float(line[6]))
            individual.append(float(line[7]))
            individual.append(float(line[8]))
            individual.append(float(line[9]))

            # Month
            individual.append(month[line[10]])

            # Google analytic data 
            individual.append(int(line[11]))
            individual.append(int(line[12]))
            individual.append(int(line[13]))
            individual.append(int(line[14]))

            individual.append(1 if line[15]== 'Returning_Visitor' else 0)
            individual.append(1 if line[16] == 'TRUE' else 0)

            # Add the label
            data[1].append(1 if line[17] == 'TRUE' else 0)


            # Adds every information to data 
            data[0].append(individual)
    
    return data
        


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors=1)

    classifier.fit(evidence,labels)

    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    # Iterar sobre os rótulos verdadeiros e previstos
    for true_label, predicted_label in zip(labels, predictions):
        if true_label == 1 and predicted_label == 1:
            true_positives += 1
        elif true_label == 0 and predicted_label == 0:
            true_negatives += 1
        elif true_label == 1 and predicted_label == 0:
            false_negatives += 1
        elif true_label == 0 and predicted_label == 1:
            false_positives += 1

    # Calcular sensibilidade
    sensitivity = true_positives / (true_positives + false_negatives)

    # Calcular especificidade
    specificity = true_negatives / (true_negatives + false_positives)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
