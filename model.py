import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class MarketingMixModel:
    def __init__(self, channels, alpha_ridge=1.0):
        """
        channels: list of string names for paid media columns
        alpha_ridge: regularization strength for Ridge regression
        """
        self.channels = channels
        self.alpha_ridge = alpha_ridge
        self.pipeline = None
        self.coefficients = {}
        self.intercept = 0.0

    def adstock_transform(self, x, retention_rate):
        """
        Applies geometric adstock transformation to model advertising carryover effect.
        retention_rate (alpha): float between 0 and 1
        """
        adstocked = np.zeros_like(x, dtype=float)
        adstocked[0] = x[0]
        for t in range(1, len(x)):
            adstocked[t] = x[t] + retention_rate * adstocked[t - 1]
        return adstocked

    def saturation_transform(self, x, half_saturation, slope):
        """
        Applies Hill function saturation curve to model diminishing returns.
        """
        return (x ** slope) / ((half_saturation ** slope) + (x ** slope))

    def preprocess_features(self, df, adstock_params, saturation_params):
        """
        Transforms raw media spend data using Adstock and Saturation parameters.
        adstock_params: dict mapping channel -> retention rate (0 to 1)
        saturation_params: dict mapping channel -> (half_saturation, slope)
        """
        processed_df = df.copy()
        
        for channel in self.channels:
            # 1. Adstock transformation
            r = adstock_params.get(channel, 0.5)
            adstocked_col = self.adstock_transform(processed_df[channel].values, r)
            
            # 2. Saturation transformation
            hs, s = saturation_params.get(channel, (np.mean(adstocked_col), 1.0))
            processed_df[channel] = self.saturation_transform(adstocked_col, hs, s)
            
        return processed_df

    def fit(self, df, target_col, adstock_params, saturation_params):
        """
        Fits the Ridge regression model on transformed media features.
        """
        # Transform data
        transformed_df = self.preprocess_features(df, adstock_params, saturation_params)
        
        X = transformed_df[self.channels]
        y = transformed_df[target_col]
        
        # Build and fit pipeline with standard scaling
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('ridge', Ridge(alpha=self.alpha_ridge))
        ])
        
        self.pipeline.fit(X, y)
        
        # Extract coefficients
        ridge_model = self.pipeline.named_steps['ridge']
        self.intercept = ridge_model.intercept_
        self.coefficients = dict(zip(self.channels, ridge_model.coef_))
        
        return self.coefficients

    def predict(self, df, adstock_params, saturation_params):
        """
        Generates sales/conversion predictions using the fitted model.
        """
        transformed_df = self.preprocess_features(df, adstock_params, saturation_params)
        X = transformed_df[self.channels]
        return self.pipeline.predict(X)