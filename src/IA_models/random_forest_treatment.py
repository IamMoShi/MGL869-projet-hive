from configparser import ConfigParser

import pandas as pd
import shap
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

from src.IA_models.KFold_XY import KFold_XY
from src.IA_models.fit_model_silently import fit_model_silently


def random_forest_treatment(title, raw_data: pd.DataFrame) -> tuple:
    config: ConfigParser = ConfigParser()
    config.read("config.ini")
    N_SPLITS: int = int(config["IA"]["NSplits"])
    SHUFFLE: bool = config["IA"].getboolean("Shuffle")
    RANDOM_STATE: int = int(config["IA"]["RandomState"])
    N_ESTIMATORS: int = int(config["IA"]["nEstimators"])

    X = raw_data.drop(columns=['BugStatus', 'Name', 'Kind'])  # variables indépendantes
    X = X.dropna(axis=1)
    y = raw_data['BugStatus']  # présence d'un bug

    X_train, X_test, y_train, y_test = KFold_XY(N_SPLITS, SHUFFLE, RANDOM_STATE, X, y)

    model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    fit_model_silently(model, X_train, y_train)
    y_pred = model.predict(X_test)

    auc = roc_auc_score(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    print(f"AUC Random Forest: {auc}")

    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)

    shap.plots.bar(shap_values, show=False)
    plt.title(f"Classement des variables par importance - {title}")
    plt.savefig(f"randomForest_{title}_shap.png")
    plt.show()

    return model, shap_values, X_train, X_test, y_train, y_test