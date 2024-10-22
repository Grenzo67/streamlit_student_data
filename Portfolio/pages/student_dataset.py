import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import json
from streamlit_folium import folium_static

st.markdown("<h1 style='font-size: 40px;'>Analysis of Middle School Student Enrollment</h1>", unsafe_allow_html=True)

data = pd.read_csv("Portfolio//pages//fr-en-college-effectifs-niveau-sexe-lv.csv", sep=";", on_bad_lines='skip', encoding="utf-8")
years = data['Rentrée scolaire'].unique()
selected_year = st.selectbox("Select a Year", years)
data_filtered = data[data['Rentrée scolaire'] == selected_year]

st.markdown(f"<h3>Distribution of Students by Academic Region in {selected_year}</h3>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)

    regions_data = data_filtered.groupby(['Région académique'])['Nombre d\'élèves total'].sum().reset_index()
    top_10_regions = regions_data.sort_values(by='Nombre d\'élèves total', ascending=False).head(10)
    top_10_regions.reset_index(drop=True, inplace=True)
    top_10_regions.columns = ['Academic Region', 'Total Students']

    with col1:
        st.markdown("##### Top 10 Academic Regions by Total Students")
        st.dataframe(top_10_regions)

    with col2:
        fig_pie = px.pie(
            regions_data,
            names='Région académique',
            values="Nombre d'élèves total",
            title="Student Distribution by Academic Region",
            color_discrete_sequence=px.colors.sequential.Plasma,
            labels={'Région académique': 'Academic Region', "Nombre d'élèves total": 'Total Students'}
        )
        st.plotly_chart(fig_pie)

st.markdown("##### Total Number of Students per Department")

with open('C://Users//hupar//Documents//Efrei//M1//Data Visualization//Portfolio//pages//departements.geojson', encoding='utf-8') as f:
    geojson_deps = json.load(f)

data_filtered["Code département"] = data_filtered["Code département"].astype(str).str.zfill(3)
total_students_per_department = data_filtered.groupby("Code département")["Nombre d'élèves total"].sum().reset_index()
student_data_dict = total_students_per_department.set_index("Code département")["Nombre d'élèves total"].to_dict()

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

choropleth = folium.Choropleth(
    geo_data=geojson_deps,
    name="choropleth",
    data=total_students_per_department,
    columns=["Code département", "Nombre d'élèves total"],
    key_on="feature.properties.code",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of students per department",
    highlight=True,
).add_to(m)

for feature in geojson_deps['features']:
    dep_code = feature['properties']['code']
    dep_name = feature['properties']['nom']
    dep_code = dep_code.zfill(3)
    num_students = student_data_dict.get(dep_code, "Not available")
    fill_color = choropleth.color_scale(num_students) if num_students != "Not available" else "#000000"
    popup_text = (f"<b>Name</b>: {dep_name}<br>"
                  f"<b>Department Code</b>: {dep_code}<br>"
                  f"<b>Number of Students</b>: {num_students}")

    folium.GeoJson(
        feature,
        style_function=lambda x, fill_color=fill_color: {
            'fillColor': fill_color,
            'color': '#000000',
            'weight': 0.5,
            'fillOpacity': 0.7
        },
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
        tooltip=popup_text
    ).add_to(m)

folium_static(m)

st.markdown("---")

st.subheader("Total Distribution of Boys and Girls")
grades = ["6th", "5th", "4th", "3rd"]
girls_data = [
    data_filtered["6èmes filles"].sum(),
    data_filtered["5èmes filles"].sum(),
    data_filtered["4èmes filles"].sum(),
    data_filtered["3èmes filles"].sum()
]
boys_data = [
    data_filtered["6èmes garçons"].sum(),
    data_filtered["5èmes garçons"].sum(),
    data_filtered["4èmes garçons"].sum(),
    data_filtered["3èmes garçons"].sum()
]

df_gender_distribution = pd.DataFrame({
    "Grade Level": grades,
    "Girls": girls_data,
    "Boys": boys_data
})

col1, col2 = st.columns(2)

with col1:
    total_girls = sum(girls_data)
    total_boys = sum(boys_data)

    fig_pie = px.pie(
        values=[total_girls, total_boys],
        names=["Girls", "Boys"],
        title="Total Distribution of Boys and Girls",
        color_discrete_sequence=["#1E90FF", "#FF69B4"]
    )
    fig_pie.update_layout(width=400, height=400)
    st.plotly_chart(fig_pie, use_container_width=False)

with col2:
    fig_line = px.line(
        df_gender_distribution.melt(id_vars=["Grade Level"], var_name="Gender", value_name="Count"),
        x="Grade Level",
        y="Count",
        color="Gender",
        title="Trends in Boys and Girls Enrollment by Grade Level",
        markers=True,
        color_discrete_map={"Girls": "#FF69B4", "Boys": "#1E90FF"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

region_gender_data = data_filtered.groupby('Région académique')[["6èmes filles", "6èmes garçons", "5èmes filles", "5èmes garçons", "4èmes filles", "4èmes garçons", "3èmes filles", "3èmes garçons"]].sum().reset_index()

region_gender_data['Total Girls'] = region_gender_data["6èmes filles"] + region_gender_data["5èmes filles"] + region_gender_data["4èmes filles"] + region_gender_data["3èmes filles"]
region_gender_data['Total Boys'] = region_gender_data["6èmes garçons"] + region_gender_data["5èmes garçons"] + region_gender_data["4èmes garçons"] + region_gender_data["3èmes garçons"]
region_gender_data['Total Students'] = region_gender_data['Total Girls'] + region_gender_data['Total Boys']
region_gender_data['Percentage Boys'] = (region_gender_data['Total Boys'] / region_gender_data['Total Students']) * 100
region_gender_data['Percentage Girls'] = (region_gender_data['Total Girls'] / region_gender_data['Total Students']) * 100
region_gender_data['Percentage Difference'] = abs(region_gender_data['Percentage Boys'] - region_gender_data['Percentage Girls'])
region_gender_data['Majority Gender'] = region_gender_data.apply(
    lambda row: 'Boys' if row['Percentage Boys'] > row['Percentage Girls'] else 'Girls', axis=1
)

region_gender_data = region_gender_data.sort_values(by='Percentage Difference', ascending=False)
top_10_regions = region_gender_data.head(10)

fig_bar = px.bar(
    top_10_regions,
    x='Région académique',
    y='Percentage Difference',
    title="Top 10 Regions with the Highest Gender Percentage Inequalities (Boys vs Girls)",
    labels={'Percentage Difference': 'Percentage Difference (%)', 'Région académique': 'Academic Region'},
    color='Majority Gender',
    color_discrete_map={'Boys': '#1E90FF', 'Girls': '#FF69B4'},
)

fig_bar.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_bar)

st.markdown("---")

def calculate_language_totals(data, lv_columns):
    totals = {}
    for lang, cols in lv_columns.items():
        existing_cols = [col for col in cols if col in data.columns]
        totals[lang] = data[existing_cols].sum().sum() if existing_cols else 0
    return totals

def plot_pie_chart(df, title, colors):
    fig = px.pie(df, names='Language', values='Total', title=title, color_discrete_sequence=colors)
    fig.update_layout(width=220, height=220, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig)

def plot_bar_chart(df, title):
    fig = px.bar(df, x="Grade", y=df.columns[1:], title=title, labels={"value": "Number of Students", "Grade": "Grade Level"}, barmode="stack")
    fig.update_layout(margin=dict(l=0, r=20, t=30, b=0))
    st.plotly_chart(fig)

st.markdown("<h2 style='text-align: center;'>Language Preferences (LV1 and LV2) Across Grades</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

lv1_columns = {
    "German": ["6èmes LV1 allemand", "5èmes LV1 allemand", "4èmes LV1 allemand", "3èmes LV1 allemand"],
    "English": ["6èmes LV1 anglais", "5èmes LV1 anglais", "4èmes LV1 anglais", "3èmes LV1 anglais"],
    "Spanish": ["6èmes LV1 espagnol", "5èmes LV1 espagnol", "4èmes LV1 espagnol", "3èmes LV1 espagnol"],
    "Other": ["6èmes LV1 autres langues", "5èmes LV1 autres langues", "4èmes LV1 autres langues", "3èmes LV1 autres langues"]
}

lv2_columns = {
    "German": ["6èmes LV2 allemand", "5èmes LV2 allemand", "4èmes LV2 allemand", "3èmes LV2 allemand"],
    "English": ["6èmes LV2 anglais", "5èmes LV2 anglais", "4èmes LV2 anglais", "3èmes LV2 anglais"],
    "Spanish": ["6èmes LV2 espagnol", "5èmes LV2 espagnol", "4èmes LV2 espagnol", "3èmes LV2 espagnol"],
    "Italian": ["6èmes LV2 italien", "5èmes LV2 italien", "4èmes LV2 italien", "3èmes LV2 italien"],
    "Other": ["6ème LV2 autres langues", "5èmes LV2 autres langues", "4èmes LV2 autres langues", "3èmes LV2 autres langues"]
}

with col1:
    lv1_totals = calculate_language_totals(data_filtered, lv1_columns)
    df_lv1_pie = pd.DataFrame(list(lv1_totals.items()), columns=['Language', 'Total'])
    plot_pie_chart(df_lv1_pie, "LV1 Language Preferences", ['#FFD700', '#FF6347', '#4682B4', '#8A2BE2'])

    lv2_totals = calculate_language_totals(data_filtered, lv2_columns)
    df_lv2_pie = pd.DataFrame(list(lv2_totals.items()), columns=['Language', 'Total'])
    plot_pie_chart(df_lv2_pie, "LV2 Language Preferences", ['#FF69B4', '#1E90FF', '#32CD32', '#FF4500', '#FFD700'])

with col2:
    languages_data = {
        "Grade": ["6th", "5th", "4th", "3rd"],
        "English LV1": data_filtered[lv1_columns["English"]].sum().values,
        "German LV1": data_filtered[lv1_columns["German"]].sum().values,
        "Spanish LV1": data_filtered[lv1_columns["Spanish"]].sum().values,
        "English LV2": data_filtered[lv2_columns["English"]].sum().values,
        "German LV2": data_filtered[lv2_columns["German"]].sum().values,
        "Spanish LV2": data_filtered[lv2_columns["Spanish"]].sum().values
    }
    df_languages = pd.DataFrame(languages_data)
    plot_bar_chart(df_languages, "Language Preferences by Grade (LV1 & LV2)")

def calculate_language_distribution(data, region):
    region_data = data[data["Région académique"] == region]
    
    lv1_totals = calculate_language_totals(region_data, lv1_columns)
    lv2_totals = calculate_language_totals(region_data, lv2_columns)

    return lv1_totals, lv2_totals

regions = data_filtered["Région académique"].unique()
selected_region = st.selectbox("Select a Region", regions)

lv1_totals, lv2_totals = calculate_language_distribution(data_filtered, selected_region)

lv1_df = pd.DataFrame(list(lv1_totals.items()), columns=["Language", "Number of Students"])
lv1_df["Type"] = "LV1"

lv2_df = pd.DataFrame(list(lv2_totals.items()), columns=["Language", "Number of Students"])
lv2_df["Type"] = "LV2"

df = pd.concat([lv1_df, lv2_df])

fig = px.bar(df, x="Type", y="Number of Students", color="Language", 
             title=f"LV1 and LV2 Language Distribution in {selected_region}",
             labels={"Type": "Language Type", "Number of Students": "Number of Students"},
             barmode="stack")

st.plotly_chart(fig)

st.markdown("---")

st.subheader("Public vs. Private Schools")

enrollment_sector = data_filtered.groupby('Secteur')['Nombre d\'élèves total'].sum().reset_index()
fig1 = px.pie(enrollment_sector, values='Nombre d\'élèves total', names='Secteur',
               title='Total Enrollment in Public vs. Private Schools',
               labels={'Nombre d\'élèves total': 'Total Students'},
               height=400)

public_schools = data_filtered[data_filtered['Secteur'] == 'PUBLIC']
private_schools = data_filtered[data_filtered['Secteur'] == 'PRIVE']

public_avg = public_schools[['6èmes total', '5èmes total', '4èmes total', '3èmes total']].mean()
private_avg = private_schools[['6èmes total', '5èmes total', '4èmes total', '3èmes total']].mean()

avg_students = pd.DataFrame({
    'Level': ['6th Grade', '5th Grade', '4th Grade', '3rd Grade'],
    'Public Schools': public_avg.values,
    'Private Schools': private_avg.values
})

avg_students_melted = avg_students.melt(id_vars='Level', var_name='School Type', value_name='Average Students')

fig2 = px.bar(avg_students_melted, x='Level', y='Average Students', color='School Type',
               barmode='group', 
               title='Average Number of Students per Institution',
               labels={'Average Students': 'Average Number of Students'},
               height=400)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

schools_count = data_filtered.groupby(['Région académique', 'Secteur']).size().unstack(fill_value=0)
schools_count['Private Percentage'] = (schools_count['PRIVE'] / (schools_count['PUBLIC'] + schools_count['PRIVE'])) * 100

schools_percentage = schools_count.reset_index()
schools_percentage = schools_percentage.sort_values(by='Private Percentage', ascending=False)

fig3 = px.bar(schools_percentage, x='Région académique', y='Private Percentage',
               title='Percentage of Private Schools by Region',
               labels={'Private Percentage': 'Percentage of Private Schools'},
               height=400)
fig3.update_traces(marker_color='#0000CD')

st.plotly_chart(fig3)
