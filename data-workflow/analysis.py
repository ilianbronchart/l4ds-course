import folium
import pandas as pd
import seaborn as sns
import os
import datetime as dt
import matplotlib.pyplot as plt

now = dt.datetime.now().strftime('%d:%m:%Y-%H:%M:%S')
folder_path = f'./reports/report-{now}'

def prepare_df():
    csv_files = [f for f in os.listdir('./csv/anglo-saxon/') if f.endswith('.csv')]

    # Concatenate all CSV files into a single dataframe
    df = pd.concat([pd.read_csv('./csv/anglo-saxon/' + f) for f in csv_files])
    df['date_stolen'] = pd.to_datetime(df['date_stolen'], unit='s')
    df['colors'] = df['frame_colors'].str.split(':').apply(tuple)
    df.drop_duplicates(inplace=True)

    return df

def bikes_per_day(df):
    # Group the dataframe by day and count the number of stolen bikes per day
    daily_counts = df.groupby(df['date_stolen'].dt.date).size().reset_index(name='count')
    daily_counts['date_stolen'] = pd.to_datetime(daily_counts['date_stolen'])
    daily_counts['date_stolen'] = daily_counts['date_stolen'].dt.strftime('%m-%d')

    # Set the tick locations and labels
    tick_labels = daily_counts['date_stolen']
    tick_locs = range(len(tick_labels))

    # Create a line chart with seaborn
    fig = plt.figure()
    sns.set_style("darkgrid")
    ax = sns.lineplot(x='date_stolen', y='count', data=daily_counts)
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labels, rotation=45)
    ax.set_title('Number of Stolen Bikes per Day')
    fig = ax.get_figure()
    fig.savefig(f'{folder_path}/bikes_per_day.png')

def bikes_per_ownership_years(df):
    # Filter out rows where the year column is null
    df_copy = df[df['year'].notnull()]

    # Create a new dataframe with the calculated years since purchase column
    df_years_since_purchase = pd.DataFrame({
        'years_since_purchase': (df['date_stolen'].dt.year.max() - df_copy['year'].astype(int)),
        'count': 1
    })
    yearly_counts = df_years_since_purchase.groupby('years_since_purchase').sum().reset_index()
    order = yearly_counts.sort_values('count', ascending=False)['years_since_purchase']

    # Create a bar chart with seaborn
    sns.set_style("darkgrid")
    fig = plt.figure()
    ax = sns.barplot(x='years_since_purchase', y='count', data=yearly_counts, color='#1E90FF', order=order)
    ax.set(xlabel='Years Since Purchase', ylabel='Number of Stolen Bikes')
    ax.set_title('Number of Stolen Bikes by Years of Ownership')
    fig.savefig(f'{folder_path}/bikes_per_ownership_years.png')

def bikes_per_manufacturer(df):
    # Group the dataframe by manufacturer and count the number of stolen bikes for each manufacturer
    manufacturer_counts = df.groupby('manufacturer_name').size().reset_index(name='count')
    order = manufacturer_counts.sort_values(by='count', ascending=False)['manufacturer_name']

    # Create a bar chart with seaborn
    sns.set_style("darkgrid")
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.3)
    ax = sns.barplot(x='manufacturer_name', y='count', data=manufacturer_counts, color='#1E90FF', order=order)
    ax.set(xlabel='Manufacturer', ylabel='Number of Stolen Bikes')
    ax.set_title('Number of Stolen Bikes by Manufacturer')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    fig.savefig(f'{folder_path}/bikes_per_manufacturer.png')

def bike_locations(df):
    df_copy = df.copy()
    df_copy.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Create a map centered on the mean latitude and longitude of the stolen bikes
    map_center = [df_copy['latitude'].mean(), df_copy['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=3)

    # Add a circle marker for each stolen bike
    for index, row in df_copy.iterrows():
        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='red', fill=True, fill_color='red').add_to(m)

    # Save the map to a file
    m.save(f'{folder_path}/bike_locations.html')

def bikes_per_color(df):
    df_colors = df.explode('colors')
    color_counts = df_colors['colors'].value_counts().sort_values(ascending=False)

    # Plot the results using seaborn
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.35)
    ax = sns.barplot(x=color_counts.index, y=color_counts.values, color='#1E90FF')
    ax.set_title('Number of Stolen Bikes by Color')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    fig.savefig(f'{folder_path}/bikes_per_color.png')

# Call each function and save the resulting charts and maps to files
df = prepare_df()

if not os.path.exists('./reports'):
    os.makedirs('./reports')

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

bikes_per_day(df)
bikes_per_ownership_years(df)
bikes_per_manufacturer(df)
bikes_per_color(df)
bike_locations(df)