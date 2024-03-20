import streamlit as st
import pandas as pd
import pickle
import os


def split_file(filename, num_parts):
  """Splits a pickled file into a specified number of parts."""
  # ... (code for splitting a file as provided earlier)

def join_files(filename, num_parts):
  """Rejoins split pickle files into the original file."""
  # ... (code for rejoining files as provided earlier)

# Check if similarity1.pkl needs to be joined from split parts
if not os.path.exists("similarity1.pkl"):
    join_files("similarity1", 4)  # Assuming 4 parts were previously split

# Load the dataset
with open('job_list1.pkl', 'rb') as f:
    df = pickle.load(f)

# Load precomputed similarity scores
with open('similarity1.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

# Function to get recommendations
def get_recommendations(title, similarity_matrix=similarity_matrix, df=df, top_n=10):
    idx = df[df['jobtitle'].str.lower() == title.lower()].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_indices = [i[0] for i in sim_scores]
    return df.iloc[recommended_indices]
    
# Streamlit App
st.sidebar.header('Filter by Features')
job_desc_checkbox = st.sidebar.checkbox('Job Description', key="job_desc_checkbox")
skills_checkbox = st.sidebar.checkbox('Skills', key="skills_checkbox")
shift_checkbox = st.sidebar.checkbox('Shift', key="shift_checkbox")


st.header('Job Recommendation System')

# Dropdown to select job title
selected_job_title = st.selectbox("Select a job title:", df['jobtitle'].values)

show_recommendations = st.button('Show Recommendations')
if show_recommendations or st.session_state.job_desc_checkbox or st.session_state.skills_checkbox or st.session_state.shift_checkbox:
    recommendations = get_recommendations(selected_job_title)
    st.subheader('Top 10 Recommended Jobs:')
    for index, row in recommendations.iterrows():
        st.write("Company:", row['company'])
        st.write("Job Title:", row['jobtitle'])
        if st.session_state.job_desc_checkbox:
            st.write("Job Description:", row['jobdescription'])
        if st.session_state.skills_checkbox:
            st.write("Skills:", row['skills'])
        if st.session_state.shift_checkbox:
            st.write("Shift:", row['shift'])
        st.divider()
