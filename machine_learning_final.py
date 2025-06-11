import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
import numpy as np
import joblib

# -----------------------------------------
# 1. Daten einlesen und Features berechnen
# -----------------------------------------
path = "/home/sven/Dokumente/dhbw/studienarbeit/Studienarbeit/daten"
all_files = [f for f in os.listdir(path) if f.startswith("packet_") and f.endswith(".csv")]

data = []
labels = []

for file in all_files:
    df = pd.read_csv(os.path.join(path, file))
    cols = df.drop(columns=['Timer', 'id']).columns
    stat_names = ['mean', 'std', 'min', 'max']
    feature_names = [f"{stat}_{col}" for stat in stat_names for col in cols]

    features = df.drop(columns=['Timer', 'id']).agg(['mean', 'std', 'min', 'max']).values.flatten()
    data.append(features)

    label = file.split("_")[-1].replace(".csv", "")
    labels.append(label)

X = pd.DataFrame(data, columns=feature_names)
y = labels

# ---------------------------
# 2. Label-Encoding & Check
# ---------------------------
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Klassenverteilung anzeigen
print("Verteilung der Klassen (vor dem Split):")
print(pd.Series(y).value_counts())

# -------------------------------
# 3. Cross-Validation & Training
# -------------------------------
clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(clf, X, y_encoded, cv=cv, scoring='accuracy')
print("\nCross-Validation Accuracy Scores:", scores)
print("Durchschnittliche Genauigkeit: {:.2f} ± {:.2f}".format(np.mean(scores), np.std(scores)))

# -------------------------------
# 4. Klassifikationsreport & CM
# -------------------------------
y_pred_cv = cross_val_predict(clf, X, y_encoded, cv=cv)

print("\nKlassifikationsreport (Cross-Validation):")
print(classification_report(y_encoded, y_pred_cv, target_names=le.classes_))

cm = confusion_matrix(y_encoded, y_pred_cv)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix (Cross-Validation)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix_cv.png")
plt.show()

# -----------------------
# 5. Modell final trainieren
# -----------------------
clf.fit(X, y_encoded)
joblib.dump(clf, "modell.pkl")
joblib.dump(le, "label_encoder.pkl")

# ----------------------------
# 6. Feature Importance Plot
# ----------------------------
feature_importances = clf.feature_importances_
indices = np.argsort(feature_importances)[::-1]
features = X.columns

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), feature_importances[indices], align="center")
plt.xticks(range(X.shape[1]), features[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.tight_layout()
plt.savefig("feature_importances.png")
plt.show()

# ----------------------------
# 7. Boxplots der Top-N Features
# ----------------------------
top_n = 10
top_features_idx = indices[:top_n]
top_features = X.columns[top_features_idx]

plt.figure(figsize=(14, 8))
for i, label in enumerate(le.classes_):
    plt.subplot(3, 1, i + 1)
    sns.boxplot(data=X.iloc[:, top_features_idx][y_encoded == i], orient="h", palette="Set2")
    plt.title(f"{label} - Top {top_n} Features", fontsize=14)
    plt.xlabel("Values", fontsize=12)
    plt.yticks(ticks=np.arange(top_n), labels=top_features, fontsize=10)
    plt.tight_layout()

plt.savefig("boxplots_cleaned.png")
plt.show()

# ----------------------------
# 8. Zeitreihenplot (standardisiert)
# ----------------------------
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

plt.figure(figsize=(14, 8))
for i, label in enumerate(le.classes_):
    class_data = X_scaled.iloc[y_encoded == i, top_features_idx]
    mean_values = class_data.mean(axis=0)
    std_values = class_data.std(axis=0)

    plt.subplot(3, 1, i + 1)
    plt.plot(top_features, mean_values, marker='o', label=f'Mean - {label}')
    plt.fill_between(top_features, mean_values - std_values, mean_values + std_values, alpha=0.3)
    plt.title(f"{label} - Zeitreihenplot (Top {top_n} Features)", fontsize=14)
    plt.ylabel("Standardized Value")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

plt.xlabel("Features")
plt.savefig("time_series_pretty.png")
plt.show()

# Boxplot der Feature-Werte für jede Klasse separat
plt.figure(figsize=(14, 8))
for i, label in enumerate(le.classes_):
    plt.subplot(3, 1, i + 1)
    sns.boxplot(data=X[y_encoded == i], orient="h", palette="Set2")
    plt.title(f"{label} - Feature Values", fontsize=14)
    plt.xlabel("Values", fontsize=12)
    plt.yticks(ticks=np.arange(len(X.columns)), labels=X.columns, fontsize=8)
    plt.tight_layout()

plt.savefig("boxplots_features_by_class_separate.png")
plt.show()


