import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler


path = "/home/sven/Dokumente/dhbw/studienarbeit/Studienarbeit/daten"
all_files = [f for f in os.listdir(path) if f.startswith("packet_") and f.endswith(".csv")]

data = []
labels = []

for file in all_files:
    df = pd.read_csv(os.path.join(path, file))

    features = df.drop(columns=['Timer', 'id']).agg(['mean', 'std', 'min', 'max']).values.flatten()
    data.append(features)

    label = file.split("_")[-1].replace(".csv", "")
    labels.append(label)

cols = df.drop(columns=['Timer', 'id']).columns
stat_names = ['mean', 'std', 'min', 'max']
feature_names = [f"{stat}_{col}" for stat in stat_names for col in cols]
X = pd.DataFrame(data, columns=feature_names)
y = labels

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred, target_names=le.classes_))

joblib.dump(clf, "modell.pkl")
joblib.dump(le, "label_encoder.pkl")

# Feature-Importance
feature_importances = clf.feature_importances_
features = X.columns
indices = np.argsort(feature_importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), feature_importances[indices], align="center")
plt.xticks(range(X.shape[1]), features[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.tight_layout()
plt.savefig("feature_importances.png")
plt.show()

# Konfusionsmatrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.show()

# Boxplots
# Select top 10 features by importance
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

# Zeitreihenplots

# Standardize X for comparability
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Plot: Mean + Std over top features for each class
top_n = 10
top_features_idx = indices[:top_n]
top_features = X.columns[top_features_idx]

plt.figure(figsize=(14, 8))

for i, label in enumerate(le.classes_):
    class_data = X_scaled.iloc[y_encoded == i, top_features_idx]
    
    # Mean and standard deviation across samples
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
