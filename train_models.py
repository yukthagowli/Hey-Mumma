from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

def create_simple_maternal_model():
    """Create a simple maternal health model"""
    # Create a simple decision tree model
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    
    # Create training data with more diverse examples
    # Format: [Age, DiastolicBP, BS, BodyTemp, HeartRate]
    X = np.array([
        # Low Risk Cases (0)
        [25, 70, 6.0, 98.2, 75],   # Young, normal BP, normal BS
        [28, 75, 6.5, 98.4, 80],   # Young adult, normal values
        [30, 80, 6.8, 98.6, 72],   # Adult, all normal
        
        # Medium Risk Cases (1)
        [35, 85, 8.0, 98.8, 88],   # Higher BS, slightly elevated BP
        [38, 88, 8.5, 99.0, 90],   # Higher age, elevated vitals
        [32, 90, 9.0, 98.9, 92],   # Elevated BP and HR
        [40, 87, 8.8, 99.1, 95],   # Higher age with elevated values
        
        # High Risk Cases (2)
        [42, 95, 11.0, 99.5, 100], # High age, BP, BS, and HR
        [39, 98, 12.0, 99.8, 105], # Very high BS and HR
        [36, 100, 10.5, 99.6, 98], # Very high BP
        [41, 92, 13.0, 99.4, 102], # Very high BS
        [45, 96, 11.5, 99.7, 108], # Multiple high risk factors
    ])
    
    # Risk levels: 0 for low, 1 for medium, 2 for high
    y = np.array([
        0, 0, 0,                 # Low risk cases
        1, 1, 1, 1,             # Medium risk cases
        2, 2, 2, 2, 2           # High risk cases
    ])
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Calculate training accuracy
    training_accuracy = model.score(X_train, y_train)
    print(f"Training Accuracy: {training_accuracy * 100:.2f}%")
    
    # Test predictions
    predictions = model.predict(X_test)
    
    # Calculate testing accuracy
    accuracy = accuracy_score(y_test, predictions)
    print(f"Testing Accuracy: {accuracy * 100:.2f}%")
    
    # Perform cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"Cross-Validation Accuracy: {cv_scores.mean() * 100:.2f}%")
    
    # Save the model
    os.makedirs('model', exist_ok=True)
    with open('model/finalized_maternal_model.sav', 'wb') as f:
        pickle.dump(model, f)
    
    # Plotting the accuracies
    accuracies = [training_accuracy * 100, accuracy * 100, cv_scores.mean() * 100]
    labels = ['Training Accuracy', 'Testing Accuracy', 'Cross-Validation Accuracy']
    plt.bar(labels, accuracies, color=['blue', 'orange', 'green'])
    plt.ylabel('Accuracy (%)')
    plt.title('Training vs Testing vs Cross-Validation Accuracy')
    plt.ylim(0, 100)
    plt.show()
    
    # Plotting in line graph
    plt.plot(labels, accuracies, marker='o', color='purple')
    plt.ylabel('Accuracy (%)')
    plt.title('Training vs Testing vs Cross-Validation Accuracy - Line Graph')
    plt.ylim(0, 100)
    plt.grid()
    plt.show()
    
    print("Maternal health model saved")

def create_maternal_prediction_model():
    """Create and evaluate the maternal prediction model"""
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    
    # Expanded training data
    X = np.array([
        [25, 70, 6.0, 98.2, 75],
        [28, 75, 6.5, 98.4, 80],
        [30, 80, 6.8, 98.6, 72],
        [35, 85, 8.0, 98.8, 88],
        [38, 88, 8.5, 99.0, 90],
        [42, 95, 11.0, 99.5, 100],
        [22, 65, 5.5, 97.5, 70],
        [29, 78, 6.2, 98.0, 77],
        [33, 82, 7.0, 98.3, 74],
        [36, 90, 9.0, 98.9, 85],
        [40, 92, 10.0, 99.2, 95],
        [45, 98, 12.0, 99.8, 105],
    ])
    y = np.array([0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2])  # Risk levels
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Calculate training accuracy
    training_accuracy = model.score(X_train, y_train)
    print(f"Training Accuracy: {training_accuracy * 100:.2f}%")
    
    # Test predictions
    predictions = model.predict(X_test)
    
    # Calculate testing accuracy
    accuracy = accuracy_score(y_test, predictions)
    print(f"Testing Accuracy: {accuracy * 100:.2f}%")
    
    # Perform K-Fold cross-validation
    kf_scores = cross_val_score(model, X, y, cv=3)
    print(f"K-Fold Cross-Validation Accuracy: {kf_scores.mean() * 100:.2f}%")
    
    # Plotting the accuracies
    accuracies = [training_accuracy * 100, accuracy * 100, kf_scores.mean() * 100]
    labels = ['Training Accuracy', 'Testing Accuracy', 'K-Fold Cross-Validation Accuracy']
    plt.bar(labels, accuracies, color=['blue', 'orange', 'green'])
    plt.ylabel('Accuracy (%)')
    plt.title('Maternal Prediction Model Accuracy')
    plt.ylim(0, 100)
    plt.show()
    
    # Plotting in line graph
    plt.plot(labels, accuracies, marker='o', color='purple')
    plt.ylabel('Accuracy (%)')
    plt.title('Maternal Prediction Model Accuracy - Line Graph')
    plt.ylim(0, 100)
    plt.grid()
    plt.show()

def create_simple_fetal_model():
    """Create a simple fetal health model"""
    # Create a simple decision tree model
    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    
    # Create training data (simplified version)
    X = np.array([
        [120, 0, 0, 0, 0, 0, 0],  # Normal
        [140, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3], # Suspect
        [160, 0.5, 0.4, 0.3, 0.2, 0.4, 0.5]  # Pathological
    ])
    y = np.array([1, 2, 3])  # 1: Normal, 2: Suspect, 3: Pathological
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Calculate training accuracy
    training_accuracy = model.score(X_train, y_train)
    print(f"Training Accuracy: {training_accuracy * 100:.2f}%")
    
    # Test predictions
    predictions = model.predict(X_test)
    
    # Calculate testing accuracy
    accuracy = accuracy_score(y_test, predictions)
    print(f"Testing Accuracy: {accuracy * 100:.2f}%")
    
    # Perform cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"Cross-Validation Accuracy: {cv_scores.mean() * 100:.2f}%")
    
    # Save the model
    os.makedirs('model', exist_ok=True)
    with open('model/fetal_health_classifier.sav', 'wb') as f:
        pickle.dump(model, f)
    
    # Plotting the accuracies
    accuracies = [training_accuracy * 100, accuracy * 100, cv_scores.mean() * 100]
    labels = ['Training Accuracy', 'Testing Accuracy', 'Cross-Validation Accuracy']
    plt.bar(labels, accuracies, color=['blue', 'orange', 'green'])
    plt.ylabel('Accuracy (%)')
    plt.title('Fetal Health Model Accuracy')
    plt.ylim(0, 100)
    plt.show()
    
    # Plotting in line graph
    plt.plot(labels, accuracies, marker='o', color='purple')
    plt.ylabel('Accuracy (%)')
    plt.title('Fetal Health Model Accuracy - Line Graph')
    plt.ylim(0, 100)
    plt.grid()
    plt.show()
    
    print("Fetal health model saved")

def create_gradient_boosting_model():
    """Create and evaluate the Gradient Boosting model"""
    model = GradientBoostingClassifier(random_state=42)
    
    # Expanded training data
    X = np.array([
        [25, 70, 6.0, 98.2, 75],
        [28, 75, 6.5, 98.4, 80],
        [30, 80, 6.8, 98.6, 72],
        [35, 85, 8.0, 98.8, 88],
        [38, 88, 8.5, 99.0, 90],
        [42, 95, 11.0, 99.5, 100],
        [22, 65, 5.5, 97.5, 70],
        [29, 78, 6.2, 98.0, 77],
        [33, 82, 7.0, 98.3, 74],
        [36, 90, 9.0, 98.9, 85],
        [40, 92, 10.0, 99.2, 95],
        [45, 98, 12.0, 99.8, 105],
    ])
    y = np.array([0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2])  # Risk levels
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Calculate training accuracy
    training_accuracy = model.score(X_train, y_train)
    print(f"Gradient Boosting Training Accuracy: {training_accuracy * 100:.2f}%")
    
    # Test predictions
    predictions = model.predict(X_test)
    
    # Calculate testing accuracy
    accuracy = accuracy_score(y_test, predictions)
    print(f"Gradient Boosting Testing Accuracy: {accuracy * 100:.2f}%")
    
    # Perform K-Fold cross-validation
    kf_scores = cross_val_score(model, X, y, cv=3)
    print(f"Gradient Boosting K-Fold Cross-Validation Accuracy: {kf_scores.mean() * 100:.2f}%")

if __name__ == "__main__":
    print("Creating models...")
    create_simple_maternal_model()
    create_maternal_prediction_model()
    create_simple_fetal_model()
    create_gradient_boosting_model()
    print("\nDone! Models have been saved in the 'model' directory.")
