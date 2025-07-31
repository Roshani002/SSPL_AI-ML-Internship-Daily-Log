import math
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots

# Plotting Functions
def check_outliers_cols_missing_values(df, cols_exist_missing_values):
    """
    Plot boxplots for columns with missing values to inspect for outliers.    
    Take df and missing value columns as argument
    """
    
    fig = make_subplots(rows=2, cols=4, subplot_titles=cols_exist_missing_values)
    for i, column in enumerate(cols_exist_missing_values):
        row = i // 4 + 1
        col = i % 4 + 1

        boxplot = px.box(df, x=column)
        for trace in boxplot.data:
            fig.add_trace(trace, row=row, col=col)
    fig.update_layout(height=1000, width=1500, showlegend=False)
    return fig


def boxplot_num_cols(df, continuous_col):
    """
    Visualize boxplot for continuos cols to detect outliers
    """
    cols = 2
    total_plots = len(continuous_col)
    rows = math.ceil(total_plots / cols)

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=continuous_col)

    for i, column in enumerate(continuous_col):
        row = i // cols + 1 
        col = i % cols + 1 

        box_fig = px.box(df, y=column)
        for trace in box_fig.data:
            fig.add_trace(trace, row=row, col=col)

    fig.update_layout(height=rows * 500, width=1200, showlegend=False)
    return fig


def lat_long_plot(df, lat, lon):
    """
    Visualise Scatter map for latitude and longitude
    """
    lat_lon_fig = px.scatter_map(df, lat, lon,hover_data='City', color_discrete_sequence=['fuchsia'], zoom=3, height=300)
    lat_lon_fig.update_layout(title=f"{lat.split('_')[0]} Location Latitude & Longitude", map_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
    return lat_lon_fig


def bar_plot_cat_cols(df, categorical_col):
    """
    Plot bar chart of all categorical cols 
    Useful for understanding distributions and dominant categories
    """
    # bar chart of all categorical cols
    cols = 2
    total_plots = len(categorical_col)
    rows = math.ceil(total_plots / cols)

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=categorical_col)

    for i, column in enumerate(categorical_col):
        row = i // cols + 1 
        col = i % cols + 1 

        column_counts = df[column].value_counts().sort_index()

        bar_fig = px.bar(x=column_counts.index, y=column_counts.values, labels = {'x': column, 'y': 'Count'})
        for trace in bar_fig.data:
            fig.add_trace(trace, row=row, col=col)

    fig.update_layout(height=rows * 500, width=1200, showlegend=False)
    return fig
