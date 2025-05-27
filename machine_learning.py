import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

path = "/path/to/daten/"
all_files = [f for f in os.listdir(path) if f.startswith("packet_") and f.endswith(".csv")]

data = []
labels = []

for file in all_files:
    df = pd.read_csv(os.path.join(path, file))

    features = df.drop(columns=['Timer', 'id']).agg(['mean', 'std', 'min', 'max']).values.flatten()
    data.append(features)

    label = file.split("_")[-1].replace(".csv", "")
    labels.append(label)

X = pd.DataFrame(data)
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
