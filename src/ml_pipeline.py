import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import joblib
import os
from datetime import datetime
import pdb

def create_and_evaluate_pipeline(X, y, save_path='models', test_size=0.2, random_state=42):
    """
    Create, evaluate and save a logistic regression pipeline with preprocessing.
    
    Parameters:
    -----------
    X : array-like of shape (n_samples, n_features)
        Training data
    y : array-like of shape (n_samples,)
        Target values (binary)
    save_path : str, default='models'
        Directory to save the model
    test_size : float, default=0.2
        Proportion of dataset to include in the test split
    random_state : int, default=42
        Random state for reproducibility
    
    Returns:
    --------
    dict
        Dictionary containing the pipeline, scores, evaluation metrics, and save path
    """
    # Create save directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Create pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(random_state=random_state))
    ])
    
    # Define hyperparameter grid for tuning
    param_grid = {
        'classifier__C': np.logspace(-4, 4, 20),
        'classifier__penalty': ['l1', 'l2'],
        'classifier__solver': ['liblinear']
    }
    
    # Create grid search
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    # Fit the grid search
    grid_search.fit(X_train, y_train)
    
    # Get best pipeline
    best_pipeline = grid_search.best_estimator_
    
    # Make predictions
    y_pred = best_pipeline.predict(X_test)
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': np.abs(best_pipeline.named_steps['classifier'].coef_[0])
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    
    # Generate timestamp for model filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f'logistic_regression_pipeline_{timestamp}.joblib'
    model_path = os.path.join(save_path, model_filename)
    
    # Save the pipeline
    joblib.dump(best_pipeline, model_path)
    
    # Save feature importance
    feature_importance.to_csv(os.path.join(save_path, f'feature_importance_{timestamp}.csv'))
    
    # Compile results
    results = {
        'pipeline': best_pipeline,
        'best_params': grid_search.best_params_,
        'best_score': grid_search.best_score_,
        'test_score': best_pipeline.score(X_test, y_test),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred),
        'feature_importance': feature_importance,
        'model_path': model_path
    }
    
    return results

def load_pipeline(model_path):
    """
    Load a saved pipeline.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model file
    
    Returns:
    --------
    sklearn.pipeline.Pipeline
        Loaded pipeline
    """
    return joblib.load(model_path)

def predict_new_data(pipeline, X_new):
    """
    Make predictions on new data using the trained pipeline.
    
    Parameters:
    -----------
    pipeline : sklearn.pipeline.Pipeline
        Trained pipeline
    X_new : array-like of shape (n_samples, n_features)
        New data to predict
    
    Returns:
    --------
    array-like
        Predictions for X_new
    """
    return pipeline.predict(X_new)

if __name__ == "__main__":
    emotion2_df = pd.read_csv("data\\features\\eeg_1738123456789_emotion2_preprocessed_emotional-features.csv", index_col=0)
    emotion2_df["emotion"] = "emotion2"
    emotion1_df = pd.read_csv("data\\features\\eeg_1738987654321_emotion1_preprocessed_emotional-features.csv", index_col=0)
    emotion1_df["emotion"] = "emotion1"
    both_emotions_df = pd.concat([emotion1_df, emotion2_df])
    X = both_emotions_df.drop('emotion', axis=1)
    y = both_emotions_df['emotion']
    results = create_and_evaluate_pipeline(X, y)
    
    # Print results
    print("Best Parameters:", results['best_params'])
    print("\nBest Cross-validation Score:", results['best_score'])
    print("\nTest Score:", results['test_score'])
    print("\nConfusion Matrix:\n", results['confusion_matrix'])
    print("\nClassification Report:\n", results['classification_report'])
    print("\nTop 5 Most Important Features:\n", results['feature_importance'].head())
    print("\nModel saved to:", results['model_path'])
    
    # Later, to load and use the saved model:
    loaded_pipeline = load_pipeline(results['model_path'])
    # Make predictions with loaded model
    # predictions = predict_new_data(loaded_pipeline, X_new)