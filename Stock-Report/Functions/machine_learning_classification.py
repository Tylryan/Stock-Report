#!/usr/bin/python

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


# Data
# This will eventually be the result of the strategy output
df = pd.read_csv('./test_crypto_data.csv', index_col='Date', parse_dates=True)


# Preprocess
# Define the features
X = df_loans.copy()
X.drop("Default", axis=1, inplace=True)


# Define the target
y = df_loans["Default"].values.reshape(-1, 1)
y[:5]

# Splitting into Train and Test sets
# Make sure random state is the same!
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=78)


# Making the date more uniform
scaler = StandardScaler()
X_scaler = scaler.fit(X_train)

X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# Model
# Creating the model
rf_model = RandomForestClassifier(n_estimators=500, random_state=78)

# Fitting the data to the model
rf_model = rf_model.fit(X_train_scaled, y_train)

# Making predictions using the test data
predictions = rf_model.predict(X_test_scaled)

# Performance
# Calculating the confusion matrix
cm = confusion_matrix(y_test, predictions)
cm_df = pd.DataFrame(
    cm, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"]
)

# Calculating the accuracy score
acc_score = accuracy_score(y_test, predictions)


# Displaying results
print("Confusion Matrix")
print(f"Accuracy Score : {acc_score}")
print("Classification Report")
print(classification_report(y_test, predictions))


# Which features have the greatest impact on the model
importances = rf_model.feature_importances_
importances_sorted = sorted(
    zip(rf_model.feature_importances_, X.columns), reverse=True)
importances_sorted[:10]
