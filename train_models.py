import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import os

# Create 'model' directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Load preprocessed data
vectorizer = joblib.load('model/vectorizer.pkl')
X_train, X_test, y_train, y_test = joblib.load('model/train_test_data.pkl')

# Define models
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'NaiveBayes': MultinomialNB(),
    'SVM': SVC(kernel='linear', probability=True)
}

# Train models and evaluate
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(f'{name} Model Evaluation:\n{classification_report(y_test, predictions)}')
    joblib.dump(model, f'model/{name}_model.pkl')
