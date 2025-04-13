import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
import os


def custom_learning_curve(model, X, Y, title):
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, Y, cv=5, scoring="neg_mean_squared_error", train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
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
    plt.title(f"Learning Curve - {title}")
    plt.legend()
    plt.savefig(f'plots/learning_curve_{title.replace(" ", "_").lower()}.png')
    plt.close()

def create_directories():
    dirs = ['models', 'results', 'plots']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def load_and_preprocess_data(data_path):
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Dataset features: {df.columns.tolist()}")
    
    targets = []
    if 'performance' in df.columns:
        targets.append('performance')
    if 'satisfation' in df.columns:  
        targets.append('satisfation')
    
    if not targets:
        raise ValueError("Target variables not found")
    
    print(f"Target variables: {targets}")
    
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
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])
    
    return X_train, X_test, scaler

def train_default_model(X_train, y_train):
    # Train a RandomForestRegressor model with default parameters
    start_time = time()
    
    print("Training RandomForestRegressor with default parameters...")
    model = RandomForestRegressor(
        n_estimators=100,  # Default parameter
        max_depth=None,    # Default parameter
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    training_time = time() - start_time
    print(f"Default model training completed in {training_time:.2f} seconds")
    
    return model, training_time

def train_optimized_model(X_train, y_train):
    # Train a RandomForestRegressor model with GridSearchCV
    start_time = time()
    
    print("Performing grid search for hyperparameter tuning...")
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestRegressor(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    print(f"Best parameters found: {best_params}")
    
    model = grid_search.best_estimator_
    
    training_time = time() - start_time
    print(f"Optimized model training completed in {training_time:.2f} seconds")
    
    return model, training_time, best_params

def evaluate_model(model, X_test, y_test, model_name):
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
    
    print(f"\nPerformance Metrics for {model_name}:")
    for target, metric_values in metrics.items():
        print(f"\n{target}:")
        for metric_name, value in metric_values.items():
            print(f"  {metric_name}: {value}")
    
    return y_pred, metrics

def feature_importance(model, X, model_name):
    """Analyze and visualize feature importance"""
    feature_importances = model.feature_importances_
    feature_names = X.columns
    
    # Sort features by importance
    indices = np.argsort(feature_importances)[::-1]
    
    # Select top 20 features for visualization
    top_n = min(20, len(feature_names))
    top_indices = indices[:top_n]
    
    plt.figure(figsize=(10, 6))
    plt.title(f'Top Feature Importances - {model_name}')
    plt.bar(range(top_n), feature_importances[top_indices])
    plt.xticks(range(top_n), [feature_names[i] for i in top_indices], rotation=90)
    plt.tight_layout()
    plt.savefig(f'plots/feature_importance_{model_name.lower().replace(" ", "_")}.png')
    plt.close()
    
    # Return top 10 important features
    top_features = [(feature_names[i], feature_importances[i]) for i in indices[:10]]
    print(f"\nTop 10 Important Features for {model_name}:")
    for feature, importance in top_features:
        print(f"{feature}: {importance:.4f}")
    
    return top_features

def save_results(models_dict, scaler, metrics_dict, top_features_dict):
    """Save models, scaler, metrics, and feature importance"""
    # Save models and scaler
    for model_name, model in models_dict.items():
        joblib.dump(model, f'models/student_performance_model_{model_name.lower().replace(" ", "_")}.pkl')
    
    if scaler is not None:
        joblib.dump(scaler, 'models/feature_scaler.pkl')
    
    # Save metrics to CSV
    all_metrics_df = pd.DataFrame()
    for model_name, metrics in metrics_dict.items():
        metrics_df = pd.DataFrame()
        for target, metric_values in metrics.items():
            for metric_name, value in metric_values.items():
                metrics_df.loc[target, metric_name] = value
        metrics_df['Model'] = model_name
        all_metrics_df = pd.concat([all_metrics_df, metrics_df], ignore_index=False)
    
    all_metrics_df.to_csv('results/model_metrics_comparison.csv')
    
    # Save top features to CSV
    for model_name, top_features in top_features_dict.items():
        features_df = pd.DataFrame(top_features, columns=['Feature', 'Importance'])
        features_df['Model'] = model_name
        features_df.to_csv(f'results/feature_importance_{model_name.lower().replace(" ", "_")}.csv', index=False)
    
    print("\nResults saved to disk:")
    for model_name in models_dict.keys():
        print(f"- {model_name} Model: models/student_performance_model_{model_name.lower().replace(' ', '_')}.pkl")
    if scaler is not None:
        print("- Scaler: models/feature_scaler.pkl")
    print("- Metrics Comparison: results/model_metrics_comparison.csv")
    for model_name in top_features_dict.keys():
        print(f"- {model_name} Feature Importance: results/feature_importance_{model_name.lower().replace(' ', '_')}.csv")

def plot_predictions(y_test, y_preds_dict, targets):
    """Create scatter plots of predicted vs actual values for multiple models"""
    for i, target in enumerate(targets):
        plt.figure(figsize=(10, 8))
        
        colors = ['blue', 'red']
        markers = ['o', 'x']
        
        for (model_name, y_pred), color, marker in zip(y_preds_dict.items(), colors, markers):
            plt.scatter(y_test.iloc[:, i], y_pred[:, i], alpha=0.5, color=color, marker=marker, label=model_name)
        
        plt.plot([y_test.iloc[:, i].min(), y_test.iloc[:, i].max()], 
                [y_test.iloc[:, i].min(), y_test.iloc[:, i].max()], 
                'k--', lw=2)
        plt.xlabel(f'Actual {target}')
        plt.ylabel(f'Predicted {target}')
        plt.title(f'Actual vs Predicted {target} - Model Comparison')
        plt.legend()
        plt.savefig(f'plots/{target}_predictions_comparison.png')
        plt.close()

def compare_model_performance(metrics_dict, targets):
    """Create bar plots comparing model performance metrics"""
    # For each target and metric, create a comparison bar plot
    for target in targets:
        # Create a figure with multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        metrics = ['MAE', 'MSE', 'RMSE', 'R2']
        
        for i, metric in enumerate(metrics):
            # Extract values for this metric and target from all models
            model_names = []
            metric_values = []
            
            for model_name, model_metrics in metrics_dict.items():
                model_names.append(model_name)
                metric_values.append(model_metrics[target][metric])
            
            # Create bar plot
            axes[i].bar(model_names, metric_values, color=['blue', 'red'])
            axes[i].set_title(f'{metric} for {target}')
            axes[i].set_ylabel(metric)
            
            # Add values on top of bars
            for j, value in enumerate(metric_values):
                axes[i].text(j, value, str(value), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'plots/metrics_comparison_{target}.png')
        plt.close()
    
    # Create a summary plot comparing performance across models
    summary_data = []
    for model_name, model_metrics in metrics_dict.items():
        for target in targets:
            for metric, value in model_metrics[target].items():
                summary_data.append({
                    'Model': model_name,
                    'Target': target,
                    'Metric': metric,
                    'Value': value
                })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Plot summary for each metric
    for metric in ['MAE', 'MSE', 'RMSE', 'R2']:
        metric_df = summary_df[summary_df['Metric'] == metric]
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Target', y='Value', hue='Model', data=metric_df)
        plt.title(f'Model Comparison - {metric}')
        plt.ylabel(metric)
        plt.savefig(f'plots/model_comparison_{metric.lower()}.png')
        plt.close()

def main():
    """Main function to run the entire pipeline"""
    # Create directories
    create_directories()
    
    # Set data path
    data_path = 'data/processed/processed_student_data.csv'
    
    # Load and preprocess data
    df, targets, num_cols = load_and_preprocess_data(data_path)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(df, targets)
    
    # Scale numerical features
    X_train, X_test, scaler = scale_numerical_features(X_train, X_test, num_cols)
    
    # Train default model (without GridSearch)
    default_model, default_time = train_default_model(X_train, y_train)
    
    # Train optimized model (with GridSearch)
    optimized_model, optimized_time, best_params = train_optimized_model(X_train, y_train)
    
    # Generate learning curves
    custom_learning_curve(default_model, X_train, y_train, "Default Model")
    custom_learning_curve(optimized_model, X_train, y_train, "Optimized Model")
    
    # Evaluate models
    default_y_pred, default_metrics = evaluate_model(default_model, X_test, y_test, "Default Model")
    optimized_y_pred, optimized_metrics = evaluate_model(optimized_model, X_test, y_test, "Optimized Model")
    
    # Store models, predictions and metrics in dictionaries
    models_dict = {
        "Default Model": default_model,
        "Optimized Model": optimized_model
    }
    
    y_preds_dict = {
        "Default Model": default_y_pred,
        "Optimized Model": optimized_y_pred
    }
    
    metrics_dict = {
        "Default Model": default_metrics,
        "Optimized Model": optimized_metrics
    }
    
    # Analyze feature importance for both models
    default_top_features = feature_importance(default_model, X_train, "Default Model")
    optimized_top_features = feature_importance(optimized_model, X_train, "Optimized Model")
    
    top_features_dict = {
        "Default Model": default_top_features,
        "Optimized Model": optimized_top_features
    }
    
    # Plot predictions
    plot_predictions(y_test, y_preds_dict, targets)
    
    # Compare model performance
    compare_model_performance(metrics_dict, targets)
    
    # Save results
    save_results(models_dict, scaler, metrics_dict, top_features_dict)
    
    # Print training time comparison
    print("\nTraining Time Comparison:")
    print(f"Default Model: {default_time:.2f} seconds")
    print(f"Optimized Model: {optimized_time:.2f} seconds")
    print(f"Time Difference: {optimized_time - default_time:.2f} seconds")
    
    # Print optimized model parameters
    print("\nOptimized Model Parameters:")
    for param, value in best_params.items():
        print(f"{param}: {value}")
    
    print("\nTraining and evaluation pipeline completed successfully!")

if __name__ == "__main__":
    main()