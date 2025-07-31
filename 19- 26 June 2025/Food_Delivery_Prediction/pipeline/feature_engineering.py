import numpy as np
import pandas as pd
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Feature Creation
def calculate_dis(df):
    """"
    Calculates the geodesic distance between restaurant and delivery locations
    Returns modified df
    """
    df['Distance_in_km'] = np.zeros(len(df))
    resturant_coordinates = df[['Restaurant_latitude', 'Restaurant_longitude']].to_numpy()
    delivery_location_coordinates = df[['Delivery_location_latitude', 'Delivery_location_longitude']].to_numpy()
    df['Distance_in_km'] = np.array([geodesic (resturant, delivery) for resturant, delivery in zip(resturant_coordinates, delivery_location_coordinates)])
    df['Distance_in_km'] = df['Distance_in_km'].astype("str").str.extract('(\d+)').astype("int64")
    return df


def calculate_time_diff(df):
    """
    Combines order date with time columns to compute 'Order_prepare_time (minutes)'.
    Handles next-day wrap-around and fills any missing values using median.
    Returns DataFrame with new columns: 'Time_Orderd_full', 'Time_Order_picked_full', and preparation time.
    """
    PREP_TIME_COL = 'Order_prepare_time (minutes)'
    df['Time_Orderd_full'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Orderd'].astype(str))
    df['Time_Order_picked_full'] = pd.to_datetime(df['Order_Date'].astype(str) + ' ' + df['Time_Order_picked'].astype(str))

    # Handle midnight wrap-around 
    df['Time_Order_picked_full'] += pd.to_timedelta(
        (df['Time_Order_picked_full'] < df['Time_Orderd_full']).astype(int), unit='D'
    )
    # Order Prep time
    df[PREP_TIME_COL] = (df['Time_Order_picked_full'] - df['Time_Orderd_full']).dt.total_seconds() / 60
    # Handle null values by filling with the median
    df[PREP_TIME_COL] = df[PREP_TIME_COL].clip(lower=0)
    df[PREP_TIME_COL].fillna(df[PREP_TIME_COL].median(), inplace=True)
    return df

def extract_data_order_date_cols(df):
    """
    - Calculates 'Order_prepare_time'.
    - Extracts day, month, hour and minutes from timestamps and date
    Drop original date time cols
    """
    df['Order_Day'] = df['Order_Date'].dt.day
    df['Order_Month'] = df['Order_Date'].dt.month
    df["Order_Year"] = df['Order_Date'].dt.year

    df['Orderd_hour'] = df['Time_Orderd'].dt.hour
    df['Orderd_minutes'] = df['Time_Orderd'].dt.minute
    df['Order_picked_hour'] = df['Time_Order_picked'].dt.hour
    df['Order_picked_minutes'] = df['Time_Order_picked'].dt.minute

    original_time_date_cols = ['Time_Orderd', 'Time_Order_picked']
    df.drop(columns=original_time_date_cols, axis=1, inplace=True)
    return df


# Feature Transformation (Grouping and Encoding)
def handle_cat_cols(df):
    print("\nBefore Grouping")
    print("\nOriginal 'City' counts:")
    print(df['City'].value_counts())

    # Handle 'City': Manually merging 'Semi-Urban' into 'Urban'
    df['City'] = df['City'].str.strip().replace({'Semi-Urban': 'Urban'})
    print("\n\nAfter Grouping")
    print("\n'City' counts after merging 'Semi-Urban':")
    print(df['City'].value_counts())

    print("\nBefore Grouping")
    print(df['Type_of_vehicle'].value_counts())
    df['Type_of_vehicle'] = df['Type_of_vehicle'].str.strip().replace({'bicycle': 'Other_Vehicle'})
    print("\n\nAfter Grouping")
    print(df['Type_of_vehicle'].value_counts())
    return df

def label_encoding(df):
    """
    Perform label encoding on Road_traffic_density col using sklearn LabelEncoder
    """
    label_enc_col = ['Road_traffic_density']
    labelencoders = {}

    for col in label_enc_col:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        labelencoders[col] = le
    df = df.drop(columns=label_enc_col)
    return df

def one_hot_encoding(df):
    """
    Perform One hot encoding on following cols using sklearn OneHotEncoder
    """
    onehot_columns = ['Weatherconditions', 'Type_of_order', 'Type_of_vehicle','Festival', 'City']

    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  
    encoded_array = encoder.fit_transform(df[onehot_columns])
    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(onehot_columns))
    encoded_df.index = df.index
    df = df.drop(columns=onehot_columns)
    df = pd.concat([df, encoded_df], axis=1)
    return df


