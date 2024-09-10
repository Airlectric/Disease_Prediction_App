import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from itertools import combinations
from collections import Counter
from sklearn.decomposition import PCA
from scipy.stats import chi2_contingency

# Set Streamlit page configuration
st.set_page_config(page_title="Health Data EDA", layout="wide")

# Title and introduction
st.title("🚀 Exploratory Data Analysis (EDA) for Health Dataset")
st.write("""
Welcome to the **Exploratory Data Analysis** section of this app! Dive deep into the dataset to uncover insights, 
understand symptom prevalence, and explore the distribution of different prognoses. Use the interactive elements to 
filter and visualize the data according to your interests. 💡
""")

# Load the dataset from the 'archive' folder
@st.cache_data
def load_data():
    dataset_path = 'archive/Training.csv'
    data = pd.read_csv(dataset_path)
    # Drop irrelevant columns
    if 'Unnamed: 133' in data.columns:
        data.drop('Unnamed: 133', axis=1, inplace=True)
    return data

dataset = load_data()

# Convert 'prognosis' to categorical type
dataset['prognosis'] = dataset['prognosis'].astype('category')


# 1. Dataset Preview
st.subheader("🔍 Dataset Preview")
st.dataframe(dataset.head(10))  # Showing top 10 rows for a better preview

# 2. Dataset Information
st.subheader("📊 Dataset Information")
buffer = pd.DataFrame(dataset.dtypes, columns=['Data Type'])
buffer['Null Values'] = dataset.isnull().sum()
st.dataframe(buffer)

# 3. Summary Statistics
st.subheader("🔢 Summary Statistics")
st.write(dataset.describe())

# 4. Top 10 Most Frequent Symptoms
st.subheader("💡 Top 10 Most Frequent Symptoms")
# Exclude 'prognosis' from features
symptom_features = dataset.columns.drop(['prognosis']).tolist()
symptom_sums = dataset[symptom_features].sum().sort_values(ascending=False)

# Bar plot for top 10 symptoms
plt.figure(figsize=(10, 6))
sns.barplot(x=symptom_sums.index[:10], y=symptom_sums.values[:10], palette="viridis")
plt.title('Top 10 Most Frequent Symptoms')
plt.xlabel('Symptoms')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# 5. Prognosis Distribution
st.subheader("🏥 Prognosis Distribution")
plt.figure(figsize=(12, 6))
sns.countplot(y='prognosis', data=dataset, order=dataset['prognosis'].value_counts().index, palette="magma")
plt.title('Count of Each Prognosis')
plt.xlabel('Count')
plt.ylabel('Prognosis')
plt.tight_layout()
st.pyplot(plt)

# 6. Symptom Correlation Heatmap
st.subheader("🔗 Symptom Correlation Heatmap")
# Due to the large number of symptoms, we'll compute a correlation matrix for the top 20 symptoms
top_20_symptoms = symptom_sums.index[:20]
corr_matrix = dataset[top_20_symptoms].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix of Top 20 Symptoms')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
st.pyplot(plt)

# 7. Prognosis-wise Symptom Analysis
st.subheader("🔍 Prognosis-wise Symptom Analysis")
prognosis_options = st.multiselect(
    "Select Prognosis to Analyze",
    options=dataset['prognosis'].unique(),
    default=dataset['prognosis'].unique()
)

if prognosis_options:
    filtered_data = dataset[dataset['prognosis'].isin(prognosis_options)]
    # Sum symptoms for selected prognoses
    prognosis_symptom_sums = filtered_data[symptom_features].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=prognosis_symptom_sums.index[:10], y=prognosis_symptom_sums.values[:10], palette="Set2")
    plt.title('Top 10 Symptoms for Selected Prognoses')
    plt.xlabel('Symptoms')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# 8. Interactive Filtering by Symptoms
st.subheader("🎯 Filter Dataset by Symptoms")

# Multiselect widget for symptoms
selected_symptoms = st.multiselect(
    "Select Symptoms to Filter By",
    options=symptom_features,  # Assuming symptom_features contains all symptom columns
    default=None
)

if selected_symptoms:
    # Filter data where all selected symptoms are present (assuming 1 indicates presence)
    filter_condition = (dataset[selected_symptoms] == 1).all(axis=1)
    filtered_data = dataset[filter_condition]

    # Display filtered dataset
    st.write(f"Displaying {len(filtered_data)} records with selected symptoms: **{', '.join(selected_symptoms)}**")
    st.dataframe(filtered_data.head())

    # Show prognosis distribution for filtered data if any records are found
    if not filtered_data.empty:
        st.subheader("🏥 Prognosis Distribution for Selected Symptoms")
        plt.figure(figsize=(12, 6))
        sns.countplot(y='prognosis', data=filtered_data, order=filtered_data['prognosis'].value_counts().index, palette="magma")
        plt.title('Prognosis Count for Selected Symptoms')
        plt.xlabel('Count')
        plt.ylabel('Prognosis')
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No records found with the selected symptoms.")


# 9. Word Cloud for Prognosis
st.subheader("🌟 Word Cloud of Prognosis")
prognosis_text = ' '.join(dataset['prognosis'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(prognosis_text)

plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Prognosis', fontsize=20)
st.pyplot(plt)

# 10. Class Imbalance Visualization
st.subheader("⚖️ Class Imbalance in Prognosis")
prognosis_counts = dataset['prognosis'].value_counts()
plt.figure(figsize=(12, 6))
sns.barplot(x=prognosis_counts.index, y=prognosis_counts.values, palette="Set3")
plt.title('Class Distribution of Prognosis')
plt.xlabel('Prognosis')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(plt)

# 11. Most Common Symptom Combinations
st.subheader("🔄 Most Common Symptom Combinations")
# Find the most common symptom pairs
symptom_pairs = combinations(symptom_features, 2)
pair_counts = Counter()

for pair in symptom_pairs:
    # Count rows where both symptoms are present
    pair_counts[pair] = dataset[(dataset[pair[0]] == 1) & (dataset[pair[1]] == 1)].shape[0]

# Get top 10 most common pairs
top_10_pairs = pair_counts.most_common(10)
if top_10_pairs:
    pairs, counts = zip(*top_10_pairs)
    pair_labels = [f"{pair[0]} & {pair[1]}" for pair in pairs]

    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(pair_labels), y=list(counts), palette="Accent")
    plt.title('Top 10 Most Common Symptom Pairs')
    plt.xlabel('Symptom Pairs')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.write("No symptom pairs found.")

# 12. PCA Dimensionality Reduction
st.subheader("📉 PCA Dimensionality Reduction")
pca = PCA(n_components=2)
pca_result = pca.fit_transform(dataset[symptom_features])

pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
pca_df['Prognosis'] = dataset['prognosis']

plt.figure(figsize=(12, 8))
sns.scatterplot(x='Principal Component 1', y='Principal Component 2', hue='Prognosis', data=pca_df, palette="Set2", alpha=0.7)
plt.title('PCA of Symptoms Colored by Prognosis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# 13. Chi-Square Test Between Symptoms and Prognosis
st.subheader("📈 Chi-Square Test Between Symptoms and Prognosis")
symptom_selected = st.selectbox("Select a Symptom for Chi-Square Test", options=symptom_features)
contingency_table = pd.crosstab(dataset[symptom_selected], dataset['prognosis'])
chi2, p, dof, ex = chi2_contingency(contingency_table)

st.write(f"**Symptom:** {symptom_selected}")
st.write(f"**Chi-Square Statistic:** {chi2:.2f}")
st.write(f"**P-value:** {p:.4f}")

if p < 0.05:
    st.write("**Result:** There is a significant association between the selected symptom and prognosis.")
else:
    st.write("**Result:** There is no significant association between the selected symptom and prognosis.")

# 14. Download Filtered Data
st.subheader("💾 Download Filtered Data")
if selected_symptoms:
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

# Conclusion
st.write("### 🎉 Thank you for exploring the dataset!")
st.write("""
Use the interactive filters and visualizations above to delve deeper into the data. Whether you're 
interested in understanding symptom prevalence, exploring prognosis distributions, or uncovering 
common symptom patterns, this EDA section has you covered. 🙌
""")
