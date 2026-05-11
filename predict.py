import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("loanapproval.csv")

# Fill missing values
df = df.fillna(df.mode().iloc[0])

# Encode categorical columns
encoders = {}
categorical_cols = ["gender", "marital_status", "employment_status"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Define features in SAME ORDER as Flask
X = df[[
    "age",
    "gender",
    "marital_status",
    "annual_income",
    "loan_amount",
    "credit_score",
    "num_dependents",
    "existing_loans_count",
    "employment_status"
]]

y = df["loan_approved"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model_loan.pkl", "wb"))

# Save encoders
pickle.dump(encoders, open("encoders_loan.pkl", "wb"))

print("model.pkl and encoders.pkl created successfully ✅")