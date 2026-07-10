# ==========================================
# CareerPath AI
# College Guidance Model Training
# ==========================================

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=" * 50)
print("CareerPath AI - College Guidance Model")
print("=" * 50)

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("college_guidance.csv")

print("\nDataset Loaded Successfully.\n")

print(df.head())

print("\nTotal Records :", len(df))

# ==========================================
# Check Missing Values
# ==========================================

print("\nChecking Missing Values...\n")

print(df.isnull().sum())

# Remove empty rows if any

df = df.dropna()

print("\nRecords After Cleaning :", len(df))
# ==========================================
# Select Features and Target
# ==========================================

X = df[[
    "Skills",
    "Technologies",
    "Certification",
    "Preferred_Work"
]].copy()

y = df["Recommended_Domain"]

# ==========================================
# Label Encoding
# ==========================================

skills_encoder = LabelEncoder()
technology_encoder = LabelEncoder()
certification_encoder = LabelEncoder()
work_encoder = LabelEncoder()
domain_encoder = LabelEncoder()

X["Skills"] = skills_encoder.fit_transform(
    X["Skills"]
)

X["Technologies"] = technology_encoder.fit_transform(
    X["Technologies"]
)

X["Certification"] = certification_encoder.fit_transform(
    X["Certification"]
)

X["Preferred_Work"] = work_encoder.fit_transform(
    X["Preferred_Work"]
)

y = domain_encoder.fit_transform(y)

print("\nFeatures\n")
print(X.head())

print("\nTarget\n")
print(y[:10])

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    #stratify=y

)

print("\nTraining Records :", len(X_train))
print("Testing Records :", len(X_test))
# ==========================================
# Train Random Forest Model
# ==========================================

print("\nTraining Random Forest Model...\n")

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42,

    max_depth=8,

    min_samples_split=5,

    min_samples_leaf=2

)

model.fit(X_train, y_train)

print("Model Trained Successfully.")

# ==========================================
# Prediction
# ==========================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    y_pred

)

print(

    "\nModel Accuracy :",

    round(accuracy * 100, 2),

    "%"

)

# ==========================================
# Create models folder
# ==========================================

os.makedirs(

    "models",

    exist_ok=True

)
# ==========================================
# Save Model
# ==========================================

joblib.dump(

    model,

    "models/college_model.pkl"

)

# ==========================================
# Save Encoders
# ==========================================

encoders = {

    "skills_encoder": skills_encoder,

    "technology_encoder": technology_encoder,

    "certification_encoder": certification_encoder,

    "work_encoder": work_encoder,

    "domain_encoder": domain_encoder

}

joblib.dump(

    encoders,

    "models/college_encoders.pkl"

)

# ==========================================
# Display Encoder Classes
# ==========================================

print("\nSkills Classes")
print(skills_encoder.classes_)

print("\nTechnologies Classes")
print(technology_encoder.classes_)

print("\nCertification Classes")
print(certification_encoder.classes_)

print("\nPreferred Work Classes")
print(work_encoder.classes_)

print("\nRecommended Domain Classes")
print(domain_encoder.classes_)

# ==========================================
# Training Completed
# ==========================================

print("\n" + "=" * 50)
print("College Guidance Model Trained Successfully")
print("=" * 50)

print("\nModel Saved Successfully")
print("models/college_model.pkl")

print("\nEncoders Saved Successfully")
print("models/college_encoders.pkl")

print("\nTraining Completed.")
