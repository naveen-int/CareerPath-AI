# ==========================================
# CareerPath AI
# School Guidance Model Training
# ==========================================

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=" * 50)
print("CareerPath AI - School Guidance Model")
print("=" * 50)

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("school_guidance.csv")

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
    "Interest",
    "Favourite_Subject",
    "Preferred_Activity"
]].copy()

y = df["Recommended_Stream"]

# ==========================================
# Label Encoding
# ==========================================

interest_encoder = LabelEncoder()
subject_encoder = LabelEncoder()
activity_encoder = LabelEncoder()
stream_encoder = LabelEncoder()

X["Interest"] = interest_encoder.fit_transform(
    X["Interest"]
)

X["Favourite_Subject"] = subject_encoder.fit_transform(
    X["Favourite_Subject"]
)

X["Preferred_Activity"] = activity_encoder.fit_transform(
    X["Preferred_Activity"]
)

y = stream_encoder.fit_transform(y)

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

    stratify=y

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

print("\nModel Accuracy :",

      round(accuracy * 100, 2),

      "%")

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

    "models/school_model.pkl"

)

# ==========================================
# Save Encoders
# ==========================================

encoders = {

    "interest_encoder": interest_encoder,

    "subject_encoder": subject_encoder,

    "activity_encoder": activity_encoder,

    "stream_encoder": stream_encoder

}

joblib.dump(

    encoders,

    "models/school_encoders.pkl"

)

# ==========================================
# Display Encoder Classes
# ==========================================

print("\nInterest Classes")
print(interest_encoder.classes_)

print("\nFavourite Subject Classes")
print(subject_encoder.classes_)

print("\nPreferred Activity Classes")
print(activity_encoder.classes_)

print("\nRecommended Stream Classes")
print(stream_encoder.classes_)

# ==========================================
# Training Completed
# ==========================================

print("\n" + "=" * 50)
print("School Guidance Model Trained Successfully")
print("=" * 50)

print("\nModel Saved Successfully")
print("models/school_model.pkl")

print("\nEncoders Saved Successfully")
print("models/school_encoders.pkl")

print("\nTraining Completed.")
