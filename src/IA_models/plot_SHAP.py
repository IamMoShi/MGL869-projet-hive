import shap
from matplotlib import pyplot as plt


def plot_SHAP(model, X_train, X_test, version: str):
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)

    shap.plots.bar(shap_values, show=False)
    plt.title(f"{version = } - Importance des variables")
    plt.savefig(f'logistic_SAHP-{version[::-4]}.png')
    plt.show()
    return shap_values