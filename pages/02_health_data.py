import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to display dataset information and exploratory analysis
st.title("Exploratory Data Analysis (EDA)")

# Load the dataset from the 'achive' folder
dataset_path = 'archive/Training.csv'
dataset = pd.read_csv(dataset_path)

# Display basic dataset information
st.subheader("Dataset Preview")
st.dataframe(dataset.head())

st.subheader("Dataset Information")
buffer = pd.DataFrame(dataset.dtypes, columns=['Data Type'])
buffer['Null Values'] = dataset.isnull().sum()
st.dataframe(buffer)

st.subheader("Summary Statistics")
st.write(dataset.describe())

# Display the distribution of a random numerical column (replace 'column_name' with an actual column name)
st.subheader("Top 10 Most Frequent Symptoms")
features = dataset.columns[:20].tolist()  # Replace with your actual feature names
# Calculate the sum of each feature
symptom_sums = dataset[features].sum().sort_values(ascending=False)
# Create the bar plot
plt.figure(figsize=(6, 3))
sns.barplot(x=symptom_sums.index[:10], y=symptom_sums.values[:10])
plt.title('Top 10 Most Frequent Symptoms')
plt.xlabel('Symptoms')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
st.pyplot(plt)

# Count plot of the target variable (prognosis)
st.subheader("Count of Each Prognosis")
plt.figure(figsize=(12, 5))
sns.countplot(y='prognosis', data=dataset, order=dataset['prognosis'].value_counts().index)
plt.title('Count of Each Prognosis')
plt.xlabel('Count')
plt.ylabel('Prognosis')
st.pyplot(plt)
