import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score, roc_curve)

# ---------- 1. Load and clean ----------
df = pd.read_csv("train.csv")
df = df.drop(columns=["Unnamed: 0", "id"], errors="ignore")

print("Shape:", df.shape)
print("\nTarget distribution:\n", df["satisfaction"].value_counts())

df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].fillna(
    df["Arrival Delay in Minutes"].median()
)

# ---------- 2. Encode ----------
df["satisfaction"] = df["satisfaction"].map(
    {"neutral or dissatisfied": 0, "satisfied": 1}
)
df = pd.get_dummies(
    df, columns=["Gender", "Customer Type", "Type of Travel", "Class"],
    drop_first=True
)

X = df.drop("satisfaction", axis=1)
y = df["satisfaction"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\nTrain:", X_train.shape, "Test:", X_test.shape)

# ---------- 3. Train ----------
rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
print("\nModel trained")

# ---------- 4. Evaluate ----------
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print("\nAccuracy :", round(accuracy_score(y_test, y_pred), 4))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob), 4))
print("\nClassification Report:\n", classification_report(
    y_test, y_pred, target_names=["Neutral/Dissatisfied", "Satisfied"]))

fig, ax = plt.subplots(1, 2, figsize=(14, 5))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax[0],
            xticklabels=["Neutral/Dissat.", "Satisfied"],
            yticklabels=["Neutral/Dissat.", "Satisfied"])
ax[0].set_title("Confusion Matrix")
ax[0].set_xlabel("Predicted")
ax[0].set_ylabel("Actual")

fpr, tpr, _ = roc_curve(y_test, y_prob)
ax[1].plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test, y_prob):.3f}")
ax[1].plot([0, 1], [0, 1], "k--")
ax[1].set_title("ROC Curve")
ax[1].set_xlabel("False Positive Rate")
ax[1].set_ylabel("True Positive Rate")
ax[1].legend()

plt.tight_layout()
plt.savefig("results.png", dpi=150)
plt.show()

# ---------- 5. Feature importance ----------
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop 10 features:\n", importances.head(10))

plt.figure(figsize=(9, 7))
top = importances.head(15)[::-1]
plt.barh(top.index, top.values, color="steelblue")
plt.title("Top 15 Feature Importances")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
plt.show()
