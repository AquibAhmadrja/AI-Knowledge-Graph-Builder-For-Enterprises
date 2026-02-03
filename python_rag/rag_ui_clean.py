# rag_ui.py
import streamlit as st
from rag_core import RAGEngine
import time

# Page configuration
st.set_page_config(
    page_title="Hybrid RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 20px auto;
        max-width: 900px;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: #f0f2f6;
        color: #1f1f1f;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Clear float */
    .message-container::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        color: #666;
        font-size: 1.1rem;
    }
    
    /* Input box styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 40px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
    }
    
    /* Example questions */
    .example-question {
        background: #f8f9fa;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid #667eea;
    }
    
    .example-question:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 10px;
    }
    
    .typing-indicator span {
        height: 10px;
        width: 10px;
        margin: 0 2px;
        background-color: #667eea;
        display: inline-block;
        border-radius: 50%;
        opacity: 0.4;
        animation: typing 1.4s infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'engine' not in st.session_state:
    with st.spinner('🚀 Loading RAG Engine...'):
        st.session_state.engine = RAGEngine()

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">🤖 Hybrid RAG Chatbot</div>
    <div class="header-subtitle">Powered by Knowledge Graph + PDF + FAISS + Ollama</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 System Info")
    st.markdown("---")
    st.markdown("### 📊 Answer Insights")

    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]

        if last_msg["role"] == "assistant":
            confidence = last_msg.get("confidence", 0.0)

            st.markdown("**Confidence Score**")
            st.progress(confidence)
            st.write(f"{int(confidence * 100)}% confident")

            st.markdown("**Source Files**")
            if last_msg.get("sources"):
                for src in last_msg["sources"]:
                    st.write(f"📄 {src}")
            else:
                st.write("No source file available")
    st.info(f"**Total Messages**: {len(st.session_state.messages)}")
    
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    
    example_questions = [
        "What is the hire date of Employee_1?",
        "What is Employee_2's salary?",
        "Who sent the email to lsharis",
        "what is the leave policy of jute corporation of india?",
        "Describe how artificial intelligence is mentioned in Microsoft."
    ]
    
    for question in example_questions:
        if st.button(f"📝 {question}", key=question, use_container_width=True):
            st.session_state.temp_query = question
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This chatbot uses:
    - 🔍 FAISS for vector search
    - 🕸️ Knowledge Graph extraction
    - 🧠 Ollama (Llama 3) for generation
    - 📄 PDF document processing
    """)

# Main chat interface
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message-container">
                <div class="user-message">
                    <strong>You:</strong><br>{message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-container">
                <div class="bot-message">
                    <strong>🤖 Assistant:</strong><br>{message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Input area
col1, col2 = st.columns([6, 1])

with col1:
    # Check if there's a temp query from example questions
    if 'temp_query' in st.session_state:
        query = st.text_input(
            "Ask a question:",
            value=st.session_state.temp_query,
            placeholder="Type your question here...",
            key="query_input",
            label_visibility="collapsed"
        )
        del st.session_state.temp_query
    else:
        query = st.text_input(
            "Ask a question:",
            placeholder="Type your question here...",
            key="query_input",
            label_visibility="collapsed"
        )

with col2:
    send_button = st.button("🚀 Send", use_container_width=True)

# Handle query submission
if send_button and query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Show typing indicator
    with st.spinner(""):
        st.markdown("""
        <div class="message-container">
            <div class="bot-message">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get response from RAG engine
        result = st.session_state.engine.answer(query)
        
        # Add small delay for better UX
        time.sleep(0.5)
    
    # Add bot response to chat history
    st.session_state.messages.append({
    "role": "assistant",
    "content": result["answer"],
    "sources": result.get("sources", []),
    "confidence": result.get("confidence", 0.0)
    })
    
    # Rerun to update chat display
    st.rerun()

# Welcome message if no messages yet
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="message-container">
        <div class="bot-message">
            <strong>🤖 Assistant:</strong><br>
            Hello! I'm your Hybrid RAG assistant. I can help you find information from knowledge graphs and PDF documents. 
            Try asking me about employee details, email communications, or any other information in the system! 
            <br><br>You can use the example questions in the sidebar to get started. 😊
        </div>
    </div>
    """, unsafe_allow_html=True)