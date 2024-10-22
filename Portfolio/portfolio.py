import streamlit as st
from PIL import Image
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Enzo Greiner - Portfolio", page_icon=":briefcase:", layout="wide")

image = Image.open('Enzo.jpg')  
st.sidebar.image(image, width=200)

with open("CV ENZO.pdf", "rb") as f:  
    st.sidebar.download_button(
        label="Download my CV",
        data=f,
        file_name="Enzo_Greiner_CV.pdf",
        mime="application/pdf"
    )

st.sidebar.title("Connect with me")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/enzo-greiner/)")
st.sidebar.markdown("[GitHub](https://github.com/Grenzo67)")
st.sidebar.markdown("[Email](mailto:enzo.greiner@efrei.net)")

def add_title_with_line(title, color="orange", underline=True):
    if underline:
        st.markdown(f"""
            <h2 style='font-size: 24px; font-weight: bold;'>{title}</h2>
            <hr style='border: none; height: 2px; background-color: {color}; margin-top: -10px; margin-bottom: 20px;'/>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <h2 style='font-size: 24px; font-weight: bold;'>{title}</h2>
        """, unsafe_allow_html=True)

st.title("Enzo Greiner - Portfolio")

add_title_with_line("Welcome!", color="#FF5733")
st.write("""
Hello ! My name is Enzo Greiner, I am 21 years old and I am an M1 student in the Data AI major at Efrei Paris.
Since 2021, I have been pursuing my engineering degree, exploring topics such as machine learning, data analysis, and AI.
My goal is to contribute to impactful projects in data science, providing meaningful solutions.
""")

add_title_with_line("Educational and Professional Timeline", color="#FFBB33")

timeline_data = {
    'Event': [
        'Efrei Paris - Data Science',
        'UC Irvine - Semester Abroad',
        'Lycée Haut-Barr - High School Diploma',
        'Darty - Sales Internship',
        'GIFI - Store Internship'
    ],
    'Type': [
        'Education', 
        'Education', 
        'Education', 
        'Internship', 
        'Internship'
    ],
    'Start': [
        '2021-09-01', 
        '2023-01-01', 
        '2018-09-01', 
        '2023-01-01', 
        '2022-07-01'
    ],
    'End': [
        '2026-06-01', 
        '2023-06-01', 
        '2021-06-01', 
        '2023-02-01', 
        '2022-08-01'
    ]
}

df_timeline = pd.DataFrame(timeline_data)

fig = px.timeline(
    df_timeline, 
    x_start="Start", 
    x_end="End", 
    y="Event", 
    color="Type",
    labels={"Event": "Event", "Type": "Category"},
    width=1200,  
    height=500  
)

fig.update_yaxes(categoryorder="total ascending") 
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Events",
    template="plotly_dark",
    margin=dict(l=0, r=0, t=60, b=0)  
)

st.plotly_chart(fig)

add_title_with_line("Skills", color="#1F77B4")

data = {
    'Skill': ['Python', 'Java', 'C', 'HTML', 'CSS', 'JavaScript'],
    'Level': [5, 3, 2, 4, 3, 3]
}
df = pd.DataFrame(data)

col1, col2 = st.columns(2)

with col1:
    fig = px.line_polar(df, r='Level', theta='Skill', line_close=True,
                        range_r=[0, 5],  
                        title="Programming Skills Overview",
                        template="plotly_dark")

    fig.update_traces(fill='toself', marker=dict(color='blue'))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=True, ticks=''),
            angularaxis=dict(tickvals=[0, 1, 2, 3, 4, 5])
        )
    )

    st.plotly_chart(fig)

def display_star_rating(stars):
    stars_html = "".join(["<span style='font-size: 24px; color: gold;'>&#9733;</span>" if i < stars else "<span style='font-size: 24px; color: lightgray;'>&#9734;</span>" for i in range(5)])
    return f"<div style='display: inline-block; line-height: 1;'>{stars_html}</div>"

with col2:
    add_title_with_line("Soft Skills", color="#2CA02C", underline=False)
    soft_skills = {
        "Teamwork": 4,
        "Perseverance": 5,
        "Adaptability": 3,
        "Stress management": 3,
        "Active listening": 4
    }

    for skill, rating in soft_skills.items():
        col_left, col_right = st.columns([1, 4])
        with col_left:
            st.write(f"**{skill}:**")
        with col_right:
            st.markdown(display_star_rating(rating), unsafe_allow_html=True)

add_title_with_line("Projects", color="#FFBB33")
st.write("Here are some of the academic projects I’ve worked on:")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Kadi - Price Comparison Website")
    project1_image = Image.open('Kadi.png')  
    st.image(project1_image)
    st.write("""
    A platform comparing product prices across supermarkets. 
    """)

with col2:
    st.subheader("DocBot - Medical Chatbot")
    project2_image = Image.open('DocBot.png')  
    st.image(project2_image)
    st.write("""
    Developed a chatbot to assist doctors in diagnostics. 
    """)

with col3:
    st.subheader("DVF Data Analysis")
    project3_image = Image.open('dvf.png')  
    st.image(project3_image)
    st.write("""
    Implemented machine learning models for data analysis. 
    """)
