from sklearn.model_selection import KFold


def KFold_XY(n_splits, shuffle, random_state, X, y):
    kf = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
    for train_index, val_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[val_index]
        y_train, y_test = y.iloc[train_index], y.iloc[val_index]
    return X_train, X_test, y_train, y_test
