import streamlit as st
import pandas as pd

st.set_page_config(page_title='Análisis de Retención y Satisfacción Estudiantil', layout='wide')

st.title('Análisis de Retención y Satisfacción Estudiantil')

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data('/mnt/data/university_student_data (1).csv')

st.sidebar.header('Filtros')
year_col = 'Year'
dept_col = None
retention_col = 'Retention Rate (%)'
satisfaction_col = 'Student Satisfaction (%)'
term_col = 'Term'

if year_col and year_col in df.columns:
    years = sorted(df[year_col].dropna().unique().tolist())
    selected_year = st.sidebar.selectbox('Año', options=['Todos'] + [str(y) for y in years])
else:
    selected_year = 'Todos'

if dept_col and dept_col in df.columns:
    deps = sorted(df[dept_col].dropna().unique().tolist())
    selected_dept = st.sidebar.selectbox('Departamento', options=['Todos'] + deps)
else:
    selected_dept = 'Todos'

if term_col and term_col in df.columns:
    terms = sorted(df[term_col].dropna().unique().tolist())
    selected_term = st.sidebar.selectbox('Término', options=['Todos'] + terms)
else:
    selected_term = 'Todos'

df_filtered = df.copy()
if selected_year != 'Todos' and year_col and year_col in df.columns:
    df_filtered = df_filtered[df_filtered[year_col].astype(str)==selected_year]
if selected_dept != 'Todos' and dept_col and dept_col in df.columns:
    df_filtered = df_filtered[df_filtered[dept_col]==selected_dept]
if selected_term != 'Todos' and term_col and term_col in df.columns:
    df_filtered = df_filtered[df_filtered[term_col]==selected_term]

st.header('Datos (vista previa)')
st.dataframe(df_filtered.head(50))

st.header('Visualizaciones')

if year_col and retention_col and year_col in df.columns and retention_col in df.columns:
    st.subheader('Tendencia de la tasa de retención')
    ragg = df_filtered.groupby(year_col)[retention_col].mean().sort_index()
    st.line_chart(ragg)

if year_col and satisfaction_col and year_col in df.columns and satisfaction_col in df.columns:
    st.subheader('Satisfacción estudiantil por año')
    sagg = df_filtered.groupby(year_col)[satisfaction_col].mean().sort_index()
    st.bar_chart(sagg)

if term_col and retention_col and satisfaction_col and term_col in df.columns:
    st.subheader('Comparación Spring vs Fall')
    df_tmp = df_filtered.copy()
    df_tmp['__term_std'] = df_tmp[term_col].astype(str).str.lower()
    def classify_term(t):
        if 'spring' in t or 'prim' in t: return 'Spring'
        if 'fall' in t or 'autumn' in t or 'oto' in t: return 'Fall'
        return t.title()
    df_tmp['__term_class'] = df_tmp['__term_std'].apply(classify_term)
    comp = df_tmp.groupby('__term_class')[[retention_col, satisfaction_col]].mean()
    st.dataframe(comp)
    st.bar_chart(comp)
