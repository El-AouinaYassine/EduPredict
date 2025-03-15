import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV , learning_curve
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
import os

def custome_learning_curve(best_rf , X, Y):
    train_sizes, train_scores, val_scores = learning_curve(
    best_rf, X, Y, cv=5, scoring="neg_mean_squared_error", train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
    )

    # Convert negative MSE to positive values
    train_scores = -train_scores
    val_scores = -val_scores

    # Calculate mean and standard deviation
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    # Plot the learning curve
    plt.figure(figsize=(8, 5))
    plt.plot(train_sizes, train_mean, 'o-', color="r", label="Training Error")
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color="r")
    plt.plot(train_sizes, val_mean, 'o-', color="b", label="Validation Error")
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color="b")

    plt.xlabel("Training Set Size")
    plt.ylabel("Mean Squared Error (MSE)")
    plt.title("Learning Curve - Optimized Random Forest Regression")
    plt.legend()
    plt.show()

def create_directories():
    dirs = ['models', 'results', 'plots']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def load_and_preprocess_data(data_path):
    # Load and preprocess the student dataset
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Dataset features: {df.columns.tolist()}")
    
    # target variables
    targets = []
    if 'performance' in df.columns:
        targets.append('performance')
    if 'satisfation' in df.columns:  
        targets.append('satisfation')
    
    if not targets:
        raise ValueError("Target variables 'performance' and/or 'satisfation' not found in the dataset")
    
    print(f"Target variables: {targets}")
    
    # Identify numerical columns for scaling
    num_cols = []
    for col in ['Nationale', 'regional', 'General', 'Francais', 'Anglais']:
        if col in df.columns:
            num_cols.append(col)
    
    print(f"Numerical columns for scaling: {num_cols}")
    
    return df, targets, num_cols

def split_data(df, targets):
    # Split data into features and targets, then into train/test sets
    X = df.drop(targets, axis=1)
    y = df[targets]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Testing set size: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test

def scale_numerical_features(X_train, X_test, num_cols):
    # Scale numerical features using StandardScaler
    if not num_cols:
        print("No numerical columns to scale")
        return X_train, X_test, None
    
    scaler = StandardScaler()
    # data li type numerical shedha wdirlha scaling wredha lblastha 
    # ex: national = 14 (rj3o)-> national = 0.14 (gha mital) 
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])
    
    return X_train, X_test, scaler

def train_model(X_train, y_train, use_grid_search=True):
    # Train a RandomForestRegressor model, optionally with GridSearchCV
    start_time = time()
    
    if use_grid_search:
        print("Performing grid search for hyperparameter tuning...")
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf = RandomForestRegressor(random_state=42, n_jobs=-1)
        grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1) #cross-validation 5 
        grid_search.fit(X_train, y_train)

        best_params = grid_search.best_params_
        print(f"Best parameters found: {best_params}")
        
        model = grid_search.best_estimator_
    else:
        print("Training RandomForestRegressor with default parameters...")
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
    
    training_time = time() - start_time
    print(f"Model training completed in {training_time:.2f} seconds")
    
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    metrics = {}
    for i, col in enumerate(y_test.columns):
        mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
        mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
        
        metrics[col] = {
            'MAE': round(mae, 3),
            'MSE': round(mse, 3),
            'RMSE': round(rmse, 3),
            'R2': round(r2, 3)
        }
    
    print("\nPerformance Metrics:")
    for target, metric_values in metrics.items():
        print(f"\n{target}:")
        for metric_name, value in metric_values.items():
            print(f"  {metric_name}: {value}")
    
    return y_pred, metrics

def feature_importance(model, X):
    """Analyze and visualize feature importance"""
    feature_importances = model.feature_importances_
    feature_names = X.columns
    
    # Sort features by importance
    indices = np.argsort(feature_importances)[::-1]
    
    # Select top 20 features for visualization
    top_n = min(20, len(feature_names))
    top_indices = indices[:top_n]
    
    plt.figure(figsize=(10, 6))
    plt.title('Top Feature Importances')
    plt.bar(range(top_n), feature_importances[top_indices])
    plt.xticks(range(top_n), [feature_names[i] for i in top_indices], rotation=90)
    plt.tight_layout()
    plt.savefig('plots/feature_importance.png')
    
    # Return top 10 important features
    top_features = [(feature_names[i], feature_importances[i]) for i in indices[:10]]
    print("\nTop 10 Important Features:")
    for feature, importance in top_features:
        print(f"{feature}: {importance:.4f}")
    
    return top_features

def save_results(model, scaler, metrics, top_features):
    """Save model, scaler, metrics, and feature importance"""
    # Save model and scaler
    joblib.dump(model, 'models/student_performance_model.pkl')
    if scaler is not None:
        joblib.dump(scaler, 'models/feature_scaler.pkl')
    
    # Save metrics to CSV
    metrics_df = pd.DataFrame()
    for target, metric_values in metrics.items():
        for metric_name, value in metric_values.items():
            metrics_df.loc[target, metric_name] = value
    
    metrics_df.to_csv('results/model_metrics.csv')
    
    # Save top features to CSV
    features_df = pd.DataFrame(top_features, columns=['Feature', 'Importance'])
    features_df.to_csv('results/feature_importance.csv', index=False)
    
    print("\nResults saved to disk:")
    print("- Model: models/student_performance_model.pkl")
    if scaler is not None:
        print("- Scaler: models/feature_scaler.pkl")
    print("- Metrics: results/model_metrics.csv")
    print("- Feature Importance: results/feature_importance.csv")

def plot_predictions(y_test, y_pred, targets):
    """Create scatter plots of predicted vs actual values"""
    for i, target in enumerate(targets):
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test.iloc[:, i], y_pred[:, i], alpha=0.5)
        plt.plot([y_test.iloc[:, i].min(), y_test.iloc[:, i].max()], 
                [y_test.iloc[:, i].min(), y_test.iloc[:, i].max()], 
                'k--', lw=2)
        plt.xlabel(f'Actual {target}')
        plt.ylabel(f'Predicted {target}')
        plt.title(f'Actual vs Predicted {target}')
        plt.savefig(f'plots/{target}_predictions.png')

def main():
    """Main function to run the entire pipeline"""
    # Create directories
    create_directories()
    
    # Set data path
    data_path = 'processed_student_data.csv'
    
    # Load and preprocess data
    df, targets, num_cols = load_and_preprocess_data(data_path)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(df, targets)
    
    # Scale numerical features
    X_train, X_test, scaler = scale_numerical_features(X_train, X_test, num_cols)
    
    # Train model with grid search for large dataset
    use_grid_search = len(X_train) > 500  # Only use grid search for larger datasets
    model = train_model(X_train, y_train, use_grid_search)
    custome_learning_curve(model , X_train ,y_train)
    # Evaluate model
    y_pred, metrics = evaluate_model(model, X_test, y_test)
    
    # Analyze feature importance
    top_features = feature_importance(model, X_train)
    
    # Plot predictions
    plot_predictions(y_test, y_pred, targets)
    
    # Save results
    save_results(model, scaler, metrics, top_features)
    
    print("\nTraining and evaluation pipeline completed successfully!")

if __name__ == "__main__":
    main()