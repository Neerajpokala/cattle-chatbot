import streamlit as st
from chatbot.main_controller import CattleChatbot
# from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title="🐄 Cattle Insights Chatbot",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize chatbot
@st.cache_resource
def init_chatbot():
    return CattleChatbot()

def main():
    # Title and description
    st.title("🐄 Cattle Insights Chatbot")
    st.markdown("Ask me about your cattle's health, behavior, location, and accelerometer data!")
    
    # Initialize chatbot
    chatbot = init_chatbot()
    
    # Sidebar with information
    with st.sidebar:
        st.header("📋 How to Use")
        st.markdown("""
        **Sample Questions:**
        - What is the temperature of cow-101?
        - Is cow-102 healthy?
        - What is cow-103 doing?
        - Where is cow-101 located?
        - Show me cow-102's accelerometer data
        - What is cow-103's AccX value?
        """)
        
        st.header("🎯 Available Cows")
        # Get available cows
        try:
            cows_df = chatbot.db.get_available_cows()
            if not cows_df.empty:
                for _, cow in cows_df.iterrows():
                    st.write(f"🐄 {cow['device_id']} - {cow['cow_name']}")
            else:
                st.write("No cows found in database")
        except Exception as e:
            st.error(f"Error loading cows: {e}")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 Hi! I'm your cattle insights assistant. Ask me about your cattle's health, behavior, location, or accelerometer data!"
            }
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your cattle..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            response = chatbot.chat(prompt)
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌡️ Check Temperature"):
            sample_question = "What is the temperature of cow-101?"
            st.session_state.messages.append({"role": "user", "content": sample_question})
            response = chatbot.chat(sample_question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("🏥 Health Check"):
            sample_question = "Is cow-102 healthy?"
            st.session_state.messages.append({"role": "user", "content": sample_question})
            response = chatbot.chat(sample_question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📊 Accelerometer Data"):
            sample_question = "Show me cow-103's accelerometer data"
            st.session_state.messages.append({"role": "user", "content": sample_question})
            response = chatbot.chat(sample_question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 Chat cleared! Ask me about your cattle."
            }
        ]
        st.rerun()

if __name__ == "__main__":
    main()