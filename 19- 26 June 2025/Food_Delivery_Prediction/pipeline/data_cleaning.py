import numpy as np
import pandas as pd
from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, field_validator
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge

# Basic Cleaning and Type Conversion
def update_dtypes(df):
    """
    Update the data types of specific columns to enable numerical operations.

    - Converts 'Order_Date' to datetime
    - Convert 'Object' dtype to 'float64' of following columns : 'Delivery_person_Age', 'Delivery_person_Ratings', 'multiple_deliveries'
    """
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format="mixed")
    df['multiple_deliveries'] = df['multiple_deliveries'].astype('float64')
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype('float64')
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype('float64')
    return df

def clean_columns(df):
    """
    - Drop unnecessary ID cols
    - clean 'Weatherconditions' column 
    - If it's the training set, cleans the target variable 'Time_taken(min)'.
    """
    df.drop('ID', axis=1, inplace=True)
    df.drop('Delivery_person_ID', axis=1, inplace=True)
    df['Weatherconditions'] = df['Weatherconditions'].apply(lambda x:x.replace("conditions", "").strip())
    df['Weatherconditions'][0]  
    return df

def check_missing_values(df):
    """
    Replaces placeholder 'NaN' strings (with or without spaces) in object columns
    with actual np.nan and prints the count of missing values for each column.
    """
    for col in df.columns:
        if df[col].dtype not in['float64','datetime64[ns]', 'int64']:
            df[col] = df[col].apply(lambda x:np.nan if 'NaN' in x else x)
    print(df.isnull().sum())
    return df


# Missing Value Imputation
def fill_missing_value_mode(df, missing_value_cols):
    """
    Fills missing values with mode (most frequent value) for each specified column.
    Also prints value counts after imputation for review.
    """
    df['Delivery_person_Age'] = df['Delivery_person_Age'].fillna(df['Delivery_person_Age'].mode()[0])
    df['multiple_deliveries'] = df['multiple_deliveries'].fillna(df['multiple_deliveries'].mode()[0])
    df['Weatherconditions'] = df['Weatherconditions'].fillna(df['Weatherconditions'].mode()[0])
    df['Road_traffic_density'] = df['Road_traffic_density'].fillna(df['Road_traffic_density'].mode()[0])  
    df['Festival'] = df['Festival'].fillna(df['Festival'].mode()[0])
    df['City']= df['City'].fillna(df['City'].mode()[0])

    for col in missing_value_cols:
        print(df[col].value_counts(dropna=False))
    return df

def impute_order_time(df):
    """
    Use IterativeImputer to fill missing values in time columns based on related columns.
    """
    TIME_TAKEN_COL = 'Time_taken(minutes)'
    
    def time_to_minutes(time_str):
        try:
            # '_' for the unused 'seconds' variable
            h, m, _ = map(int, time_str.split(':'))
            return h * 60 + m
        except (ValueError, TypeError):
            return np.nan

    def minutes_to_time(mins):
        if np.isnan(mins):
            return np.nan
        h = int(mins // 60)
        m = int(mins % 60)
        return f"{h:02d}:{m:02d}:00"

    # convert time columns to minutes
    df['Time_Orderd_min'] = df['Time_Orderd'].apply(lambda x: time_to_minutes(x) if pd.notnull(x) else np.nan)
    df['Time_Order_picked_min'] = df['Time_Order_picked'].apply(time_to_minutes)

    # If time_taken column exists, use it
    cols = ['Time_Orderd_min', 'Time_Order_picked_min']
    if TIME_TAKEN_COL in df.columns:
        df[TIME_TAKEN_COL] = pd.to_numeric(df[TIME_TAKEN_COL], errors='coerce')
        cols.append(TIME_TAKEN_COL)

    # Imputation
    imputer = IterativeImputer(estimator=BayesianRidge(), max_iter=10, random_state=42)
    imputed_array = imputer.fit_transform(df[cols])
    # Restore imputed Time_Orderd
    df['Time_Orderd_imputed_min'] = imputed_array[:, 0]
    df['Time_Orderd_imputed'] = df['Time_Orderd_imputed_min'].apply(minutes_to_time)
    return df


# Outlier and Invalid Data Removal
def remove_outlier(df, column):
    """
    Remove outliers in a column using IQR method.
    """
    remove_outlier_col = [column]
    print("Old Shape", df.shape)

    for column in remove_outlier_col:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        print(f"Outlier Bounds for '{column}':")
        print(f"  Lower Bound = {lower}")
        print(f"  Upper Bound = {upper}")
            
        mask = (df[column] < lower) | (df[column] > upper)
        outlier_indices = df[mask].index
        df.drop(index=outlier_indices, inplace=True)
        print(f"{column} -> New Shape: {df.shape}")
    return df

def detect_wrong_time_data(df):
    """
    Detect wrong time data where Time_order_picked > Time_Orderd 
    Print index of wrong data
    Print shape before and after dropping wrong time data
    Remove wrong data
    """
    df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'], format='%H:%M:%S').dt.time
    df['Time_Order_picked'] = pd.to_datetime(df['Time_Order_picked'], format='%H:%M:%S').dt.time

    condition_picked_earlier = df['Time_Order_picked'] < df['Time_Orderd']
    not_late_order = df['Time_Orderd'].apply(lambda t: t.hour != 23)

    # Final "bad" rows = picked earlier AND not a late-night order
    true_bad_data_mask = condition_picked_earlier & not_late_order
    bad_rows = df[true_bad_data_mask][['Order_Date', 'Time_Orderd', 'Time_Order_picked']]
    print("\nwrong time data records")
    print(bad_rows)

    if true_bad_data_mask.any():
    # Removing bad data
        index_of_wrong_data = df[true_bad_data_mask].index
        print("index of wrong time data records", index_of_wrong_data)

        print("Shape before dropping wrong time data", df.shape)
        df.drop(index=index_of_wrong_data, inplace=True)
        print("Shape after dropping wrong time data", df.shape)
    return df

# Data Validation / Validate time data
class TimeValidator(BaseModel):
    Order_Time: Optional[time]  # will auto-parse 'HH:MM:SS'

    @field_validator('Order_Time', mode='before')
    @classmethod
    def validate_time(cls, v):
        if v in [None, '']:
            return None
        if isinstance(v, time):
            return v  # let Pydantic try to parse it into `datetime.time`
        try:
            v_str = str(v).strip()
            parts = v_str.split(':')
            if len(parts) != 3:
                return None
            # Pad each part to 2 digits: ['8', '5', '0'] → ['08', '05', '00']
            parts = [p.zfill(2) for p in parts]
            normalized = ':'.join(parts)
            parsed_time = datetime.strptime(normalized, '%H:%M:%S').time()
            return parsed_time
        except Exception:
            return None

def validate_time_row(row):
    try:
        return TimeValidator(Order_Time=row).Order_Time
    except Exception:
        return None
    
def validating_time_data(df):
    """
    Validate time data using Pydantic
    Returns modified df
    """
    df['Time_Orderd'] = df['Time_Orderd'].apply(validate_time_row)
    df['Time_Order_picked'] = df['Time_Order_picked'].apply(validate_time_row)
    print(df[['Time_Orderd', 'Time_Order_picked']].isnull().sum())
    return df
