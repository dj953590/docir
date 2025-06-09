import streamlit as st
import random
import time
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Helios CREDA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #3b82f6;
            --accent: #f59e0b;
            --background: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --text: #1e293b;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container styling */
        .appview-container .main .block-container {
            max-width: 100%;
            padding: 1rem 2rem;
        }
        
        /* Title styling */
        .main-title {
            color: var(--primary);
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border);
        }
        
        /* Document selector styling */
        .document-selector {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }
        
        /* Input section styling */
        .input-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            margin-bottom: 2rem;
        }
        
        /* Response section styling */
        .response-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }
        
        /* Feedback section styling */
        .feedback-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
        }
        
        /* Response card styling */
        .response-card {
            padding: 1.5rem;
            background: #f1f5f9;
            border-radius: 8px;
            border-left: 4px solid var(--primary);
            margin-bottom: 1rem;
        }
        
        .response-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #64748b;
        }
        
        .document-tag {
            background: var(--primary);
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        /* Button styling */
        .stButton>button {
            background: var(--primary) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
            width: 100%;
        }
        
        .stButton>button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(37,99,235,0.2);
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Feedback radio buttons */
        .stRadio>div>label {
            margin-right: 1rem;
            cursor: pointer;
        }
        
        /* Progress bar styling */
        .stProgress>div>div>div>div {
            background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Preconfigured list of credit documents
CREDIT_DOCUMENTS = [
    "Credit Agreement - ABC Corp (2023)",
    "Loan Agreement - XYZ Holdings (2024)",
    "Revolving Credit Facility - Global Industries",
    "Term Loan Agreement - Tech Innovations Inc",
    "Credit Facility Amendment - Finance Group LLC",
    "Syndicated Loan Agreement - Mega Corp",
    "Credit Line Agreement - Small Business Co",
    "Debt Financing Agreement - Startup Ventures"
]

# Simulated responses based on document and query
def generate_response(document, query):
    """Generate a simulated response based on the document and query"""
    
    # Simulate processing time
    with st.spinner("Analyzing document..."):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1)
        progress_bar.empty()
    
    # Document-specific responses
    if "interest rate" in query.lower():
        return f"The applicable interest rate in the {document} is LIBOR + 2.5%. The rate is reset quarterly."
    
    if "maturity date" in query.lower():
        return f"The maturity date specified in the {document} is December 31, 2028. This date may be extended under certain conditions."
    
    if "covenant" in query.lower():
        return f"The {document} includes financial covenants requiring the borrower to maintain:\n- Minimum liquidity of $5M\n- Debt-to-EBITDA ratio below 4.0x\n- Interest coverage ratio above 3.0x"
    
    if "collateral" in query.lower():
        return f"Under the {document}, collateral includes all business assets, including accounts receivable, inventory, and intellectual property. A first-priority lien is granted to the lender."
    
    if "default" in query.lower():
        return f"The {document} specifies events of default including:\n- Failure to make payments within 5 business days\n- Breach of covenants not cured within 30 days\n- Material adverse change in financial condition"
    
    # Generic responses
    responses = [
        f"The {document} specifies that the borrower must maintain certain financial ratios throughout the term of the agreement.",
        f"According to section 4.3 of the {document}, prepayments are allowed without penalty after the first anniversary of the agreement.",
        f"The {document} includes standard representations and warranties regarding the borrower's financial condition and legal authority.",
        f"Assignment provisions in the {document} require lender consent for any transfer of the borrower's obligations.",
        f"The governing law clause in the {document} specifies that disputes will be resolved under New York law.",
        f"Financial reporting requirements in the {document} mandate quarterly statements within 45 days of quarter-end.",
        f"Events of default in the {document} include cross-default provisions to other material debt agreements."
    ]
    
    return random.choice(responses)

def main():
    # Main title
    st.markdown('<h1 class="main-title">Helios CREDA</h1>', unsafe_allow_html=True)
    st.caption("Credit Document Expert Assistant")
    
    # Document selection
    st.markdown('<div class="document-selector">', unsafe_allow_html=True)
    st.subheader("📑 Select Credit Document")
    selected_doc = st.selectbox("Choose a document to analyze", CREDIT_DOCUMENTS)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Query input
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("💬 Ask About the Document")
    query = st.text_area(
        "Enter your natural language question about the credit agreement:",
        height=150,
        placeholder="E.g., 'What is the interest rate?' or 'Explain the covenant requirements'",
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit Question", key="submit_btn", use_container_width=True):
            if query.strip():
                st.session_state.query = query
                st.session_state.selected_doc = selected_doc
                st.session_state.response = generate_response(selected_doc, query)
                st.session_state.feedback_given = False
                st.session_state.feedback_value = None
                st.session_state.feedback_comment = ""
            else:
                st.warning("Please enter a question before submitting")
    with col2:
        if st.button("Clear Session", key="clear_btn", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display response if available
    if hasattr(st.session_state, 'response'):
        st.markdown('<div class="response-section">', unsafe_allow_html=True)
        st.subheader("📝 Response")
        
        st.markdown(f"""
            <div class="response-card">
                <div class="response-header">
                    <div>Query: <strong>{st.session_state.query}</strong></div>
                    <div class="document-tag">{st.session_state.selected_doc}</div>
                </div>
                <div>{st.session_state.response}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedback section
        st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
        st.subheader("📊 Was this response helpful?")
        
        if not st.session_state.get('feedback_given', False):
            feedback = st.radio(
                "Select your feedback:",
                ["Yes", "No"],
                index=None,
                key="feedback_radio",
                horizontal=True
            )
            
            if feedback == "No":
                st.session_state.feedback_comment = st.text_area(
                    "Please help us improve. What was missing or incorrect?",
                    height=100,
                    key="feedback_comment"
                )
            
            if feedback:
                if st.button("Submit Feedback", key="feedback_btn", use_container_width=True):
                    st.session_state.feedback_given = True
                    st.session_state.feedback_value = feedback
                    st.success("Thank you for your feedback! We'll use it to improve our responses.")
        else:
            st.success("Thank you for your feedback! We'll use it to improve our responses.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
