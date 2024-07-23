import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from etl import ibov
from datetime import timedelta

df = pd.DataFrame(ibov)
df.reset_index(inplace=True)

# Streamlit app
st.title('Ibovespa Dashboard')

# Sidebar for filtering (Filter Options)
st.sidebar.header('Filter Options')
start_date = st.sidebar.date_input('Start date', df['Date'].min())
end_date = st.sidebar.date_input('End date', df['Date'].max())

# Filter data based on user input
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# Show filtered data
st.subheader('Filtered Data')
st.write(filtered_df)

# Plotting

# Price over Time
st.subheader('Price over Time')
fig, ax = plt.subplots()
ax.fill_between(filtered_df['Date'], filtered_df['Close'], label='Close', color='skyblue', alpha=0.4)
ax.plot(filtered_df['Date'], filtered_df['Close'], color='Slateblue', alpha=0.6)
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_ylim(bottom=filtered_df['Close'].min() * 0.9, top=filtered_df['Close'].max() * 1.1)
ax.grid(True)
ax.legend()
st.pyplot(fig)


#Oscilation over Time and Median
average_oscilation = filtered_df['Oscillation'].mean()
st.subheader('Oscillation over Time')
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Oscillation'], label='Oscillation', color='green')
ax.axhline(average_oscilation, color='blue', linestyle='--', label=f'Average Oscillation: {average_oscilation:.2f}')
ax.set_xlabel('Date')
ax.set_ylabel('Oscillation')
ax.legend()
st.pyplot(fig)


#Function to filter the last five days in dataset 
def filter_last_5_days_from_latest(df, date_column):
    # Convert the date column to datetime format if it's not already
    df[date_column] = pd.to_datetime(df[date_column])
    # Find the most recent date in the dataset
    latest_date = df[date_column].max()
    # Calculate the date 5 days before the most recent date
    five_days_ago = latest_date - timedelta(days=5)
    # Filter DataFrame to include only the last 5 days
    filtered_df = df[df[date_column] >= five_days_ago]
    return filtered_df

#Calculate average oscilattion last five days
df_last_five_days = filter_last_5_days_from_latest(filtered_df, 'Date')
avg_last_five_days_oscilation = df_last_five_days['Oscillation'].mean()


#Function to filter the last twenty days in dataset 
def filter_last_twenty_days_from_latest(df, date_column):
    # Convert the date column to datetime format if it's not already
    df[date_column] = pd.to_datetime(df[date_column])
    # Find the most recent date in the dataset
    latest_date = df[date_column].max()
    # Calculate the date 5 days before the most recent date
    five_days_ago = latest_date - timedelta(days=20)
    # Filter DataFrame to include only the last 20 days
    filtered_df = df[df[date_column] >= five_days_ago]
    return filtered_df

#Calculate average oscilattion last twenty days
df_last_twenty_days = filter_last_twenty_days_from_latest(filtered_df, 'Date')
avg_last_twenty_days_oscilation = df_last_twenty_days['Oscillation'].mean()


#Function to filter the last sixty days in dataset 
def filter_last_sixty_days_from_latest(df, date_column):
    # Convert the date column to datetime format if it's not already
    df[date_column] = pd.to_datetime(df[date_column])
    # Find the most recent date in the dataset
    latest_date = df[date_column].max()
    # Calculate the date 5 days before the most recent date
    five_days_ago = latest_date - timedelta(days=60)
    # Filter DataFrame to include only the last 60 days
    filtered_df = df[df[date_column] >= five_days_ago]
    return filtered_df

#Calculate average oscilattion last five days
df_last_sixty_days = filter_last_sixty_days_from_latest(filtered_df, 'Date')
avg_last_sixty_days_oscilation = df_last_sixty_days['Oscillation'].mean()


# Create a DataFrame for the averages
averages = pd.DataFrame({
    'Period': ['Last 5 Days', 'Last 20 Days', 'Last 60 Days'],
    'Average Oscillation': [avg_last_five_days_oscilation, avg_last_twenty_days_oscilation, avg_last_sixty_days_oscilation]
})

# Plotting the bar chart
st.title("Average Oscillation Over Different Periods")
fig, ax = plt.subplots()
bars = ax.bar(averages['Period'], averages['Average Oscillation'], color=['blue', 'green', 'red'])
# Adding numbers on the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
ax.set_xlabel('Period')
ax.set_ylabel('Average Oscillation')
ax.set_title('Average Oscillation Over Different Periods')
st.pyplot(fig)