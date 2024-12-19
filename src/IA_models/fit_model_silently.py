import os
import sys
import warnings


def fit_model_silently(model, X_train, y_train):
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        # Ignorer les avertissements pendant l'entraînement
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(X_train, y_train)
        sys.stdout = sys.__stdout__  # Restaurer la sortie standard