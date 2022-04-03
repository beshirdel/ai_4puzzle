import pickle


def save(db, groups, size):
    with open('pattern_' + str(size) + '.db', 'wb') as file:
        pickle.dump(groups, file)
        pickle.dump(db, file)


def load(size):
    with open('pattern_' + str(size) + '.db', 'rb') as file:
        groups = pickle.load(file)
        db = pickle.load(file)
        return groups, db
