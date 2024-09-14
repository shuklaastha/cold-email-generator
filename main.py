import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #007BFF;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            font-weight: bold;
        }
        .footer a {
            color: white;
            text-decoration: none;
            margin: 0 10px;
        }
        .footer a:hover {
            color: #f1f1f1;
            text-decoration: underline;
        }
        /* Page title styling */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #007BFF;
            margin-bottom: 30px;
        }
        .intro-text {
            font-size: 16px;
            color: #5A5A5A;
            margin-bottom: 20px;
            text-align: center;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            margin-top: 10px;
        }
        /* Prevent button text color change on hover, active, and focus states */
        .stButton>button:hover {
            background-color: #0056b3;
            color: white;
        }
        .stButton>button:active {
            background-color: #004080;
            color: white;
        }
        .stButton>button:focus {
            outline: none;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    
    st.markdown('<div class="title">📧 Cold Mail Generator</div>', unsafe_allow_html=True)

    st.markdown('<div class="intro-text">This tool extracts job postings from a provided URL and generates personalized cold emails based on your portfolio and relevant skills.</div>', unsafe_allow_html=True)


    col1, col2 = st.columns([4, 1])
    
    with col1:
        url_input = st.text_input("Enter a URL:", value="https://www.morganstanley.com/careers/students-graduates/opportunities/17980", help="Provide the URL from which you want to extract jobs.")
    

    with col2:
        submit_button = st.button("Submit")
    
    # Process input and generate email if the submit button is pressed
    if submit_button:
        try:
            with st.spinner("Fetching job details and generating emails..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                for _, job in enumerate(jobs, start=1):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    
                    st.markdown(f"#### Generated Email for {job['role']}:")
                    st.code(email, language='markdown')
                    st.markdown("---")
        except Exception as e:
            st.error(f"An error occurred while processing: {e}")


    st.markdown("""
        <div class="footer">
            <p>&copy; 2024 Cold Mail Generator | 
            <a href="https://github.com/shuklaastha/Cold_email_generator" target="_blank"> GitHub</a> | 
            <a href="https://www.linkedin.com/in/astha-shukla-b94692233/" target="_blank">Linkedin</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
