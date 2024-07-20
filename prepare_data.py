import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import joblib
import os

# Create 'model' directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Load dataset
data = pd.read_csv('email_phishing_dataset.csv')

# Print column names to debug
print("Columns in dataset:", data.columns)

# Check if required columns exist
if 'email_content' not in data.columns or 'label' not in data.columns:
    raise ValueError("Dataset must contain 'email_content' and 'label' columns")

# Print a few rows to verify data
print(data.head())

# Preprocess text data
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['email_content'])
y = data['label']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save preprocessing objects
joblib.dump(vectorizer, 'model/vectorizer.pkl')
joblib.dump((X_train, X_test, y_train, y_test), 'model/train_test_data.pkl')

print("Data preparation complete. Preprocessing objects saved.")
