import pandas as pd

# Données sous forme brute
data = [
    [0, "2.0.0_full_metrics.csv", "Logistic Regression", 0.887378640776699, 0.45652173913043476, 0.9481327800829875, 0.26582278481012656],
    [1, "2.0.0_full_metrics.csv", "Random Forest", 0.8998073217726397, 0.6428571428571429, 0.9688796680497925, 0.34177215189873417],
    [2, "2.1.0_full_metrics.csv", "Logistic Regression", 0.9185185185185185, 0.6304347826086957, 0.9668615984405458, 0.3972602739726027],
    [3, "2.1.0_full_metrics.csv", "Random Forest", 0.9313543599257885, 0.7659574468085106, 0.9785575048732943, 0.4931506849315068],
    [4, "2.2.0_full_metrics.csv", "Logistic Regression", 0.9224283305227656, 0.6129032258064516, 0.9785330948121646, 0.2923076923076923],
    [5, "2.2.0_full_metrics.csv", "Random Forest", 0.9261744966442953, 0.75, 0.9874776386404294, 0.3230769230769231],
    [6, "2.3.0_full_metrics.csv", "Logistic Regression", 0.9968304278922345, 0.0, 0.995253164556962, 0.0],
    [7, "2.3.0_full_metrics.csv", "Random Forest", 0.9968454258675079, 0.0, 1.0, 0.0],
    [8, "3.0.0_full_metrics.csv", "Logistic Regression", 0.7719298245614035, 0.9408695652173913, 0.7951807228915663, 0.9327586206896552],
    [9, "3.0.0_full_metrics.csv", "Random Forest", 0.8971428571428571, 0.9842381786339754, 0.9457831325301205, 0.9689655172413794],
    [10, "3.1.0_full_metrics.csv", "Logistic Regression", 0.9353507565337001, 0.46153846153846156, 0.9798270893371758, 0.2033898305084746],
    [11, "3.1.0_full_metrics.csv", "Random Forest", 0.9542302357836339, 0.8125, 0.9913544668587896, 0.4406779661016949],
    [12, "4.0.0_full_metrics.csv", "Logistic Regression", 0.9328512396694215, 0.675, 0.9858078602620087, 0.29347826086956524],
    [13, "4.0.0_full_metrics.csv", "Random Forest", 0.9344933469805528, 0.9032258064516129, 0.9967248908296943, 0.30434782608695654],
]

# Colonnes
columns = ["ID", "File", "Algorithm", "Accuracy", "Precision", "Recall", "F1-Score"]

# Création du DataFrame
df = pd.DataFrame(data, columns=columns)

# Sauvegarde dans un fichier Excel
df.to_excel("full_metrics_data.xlsx", index=False)

print("Le fichier Excel 'full_metrics_data.xlsx' a été créé avec succès.")
