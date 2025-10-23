import streamlit as st


st.set_page_config(page_title="StockView360", layout="wide")
# Custom CSS to freeze header
st.markdown("""
    <style>
        .sticky-header {
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            background-color: white;
            padding: 10px 0;
            z-index: 999;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Apply sticky class to your header
st.markdown("<div class='sticky-header'><h1 style='margin:0;'>🔍 StockView360 🌐</h1></div>", unsafe_allow_html=True)


# 👤
# st.image("👤", caption="",width=150)

# Layout with image and text
col1, col2, col3 = st.columns([2, 2, 2])

# with col1:
    # st.image("img/img1.png", width=100)  # Replace with your image path or URL

with col1:
    st.markdown("""
    ### Tushar Shingade  
    🏠 Location: Pune, Mumbai, Bengaluru, Hyderabad, India  
    💼 Profession: Sr.Quant Researcher (10+ Years Experiance)  
    🎓 Education: M.Tech Engg.               
    🔗 LinkedIn:https://www.linkedin.com/in/tushar-shingade               
    ✉️ Email: tusharshingade024@gmail.com  
                
    """)
    # 🔗 GitHub: https://github.com/shingadetm

with col2:
    st.markdown("### 📊 Core Competencies")
    st.markdown("- Quantitative modeling & financial product research, Financial markets ")
    st.markdown("- Algorithmic portfolio construction & risk targeting ")
    st.markdown("- Financial instruments: Fixed Income, Equity, Indices, Bonds, Derivatives, Futures & Options ")
    st.markdown("- Statistical analysis, Machine learning toolkits, Time series analysis")
    st.markdown("- Client portfolio construction, Rebalance, Risk optimization, Tax efficient optimization ")
    st.markdown("- Regression, hypothesis testing, Bayesian inference ")





with col3:
    st.markdown("### 🧠 Skills")
    st.markdown("- Advanced Programming: Mastery of Python, R, MATLAB, VBA, SQL, and familiarity with Scala")
    st.markdown("- Machine Learning & AI: Deep understanding of supervised, unsupervised, and reinforcement learning; experience with frameworks like TensorFlow, PyTorch, and XGBoost")
    st.markdown("- Big Data Technologies: Proficiency in Hadoop, Spark, Hive, and distributed computing")
    st.markdown("- Cloud Platforms: Expertise in AWS, Azure, or Google Cloud for scalable data solutions")
    st.markdown("- Data Engineering: Building robust data pipelines using tools like Snowflake, Airflow, Kafka, and ETL frameworks")
    st.markdown("- MLOps & Model Deployment: CI/CD for ML, containerization (Docker), orchestration (Kubernetes), and monitoring models in production")

    
st.markdown("---")


# 🌱 Interests
# Financial markets
# Data visualization
# AI and automation


st.page_link("Dashboard.py", label="Go to Dashboard", icon="📊")

st.markdown("---")
st.markdown("© 2025, All rights reserved.", unsafe_allow_html=True)


