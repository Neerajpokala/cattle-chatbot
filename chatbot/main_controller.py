import streamlit as st
from .query_processor import SimpleQueryProcessor
from .sql_generator import SimpleSQLGenerator
from .response_generator import SimpleResponseGenerator
from database.connection import DatabaseConnection

class CattleChatbot:
    def __init__(self):
        self.query_processor = SimpleQueryProcessor()
        self.sql_generator = SimpleSQLGenerator()
        self.response_generator = SimpleResponseGenerator()
        self.db = DatabaseConnection()
    
    def chat(self, user_message: str) -> str:
        """Main chat method with Streamlit integration"""
        try:
            with st.spinner("🤔 Thinking..."):
                # Step 1: Process user query
                processed = self.query_processor.process_query(user_message)
                
                # Step 2: Generate SQL
                sql_query = self.sql_generator.generate_query(processed)
                
                # Show SQL query in sidebar for debugging
                with st.sidebar:
                    st.subheader("🔍 Generated SQL")
                    st.code(sql_query, language='sql')
                
                # Step 3: Execute query
                results = self.db.execute_query(sql_query)
                
                # Step 4: Generate response
                response = self.response_generator.generate_response(processed, results, self.db)
                
                return response
                
        except Exception as e:
            st.error(f"Chatbot error: {str(e)}")
            return f"🔧 Sorry, I encountered an error: {str(e)}"