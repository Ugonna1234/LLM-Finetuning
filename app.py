import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load your OpenAI API key from environment variable or pass it directly
import os
openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')

# App config
st.set_page_config(page_title="LM Studio Streaming Chatbot", page_icon="🤖")

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             opacity: 1; /* Adjust opacity value (0.0 to 1.0) */
             mix-blend-mode: multiply; /* Adjust blend mode as needed */
         }}
         </style>
         """,       
         unsafe_allow_html=True
     )

add_bg_from_url()


add_bg_from_url() 

# Container for chatbot interface
st.title("Restaurant Critic Streaming Chatbot")
st.markdown("This is where the chatbot interface goes...")

# Sidebar for LM Studio configuration
st.sidebar.title('LM Studio Advanced Configuration')
# Metadata and description of the model
st.sidebar.markdown("### Model Information")
st.sidebar.markdown("**Model Type**: froggeric/WestLake-10.7B-v2-GGUF")
st.sidebar.markdown("**Description**: This model provides a general-purpose language model capable of generating human-like text based on given input.")

##context_length = st.sidebar.slider('Context Length', min_value=20, max_value=200, value=100, step=10, help="The number of tokens (words) in the context provided to the model.")
temperature = st.sidebar.slider('Temperature', min_value=0.1, max_value=2.0, value=0.7, step=0.1, help="Controls the randomness of predictions. Lower values make the model more deterministic, while higher values make it more random.")
#tokens_to_generate = st.sidebar.slider('Tokens to Generate', min_value=10, max_value=100, value=50, step=10, help="Number of tokens (words) to generate in the response.")


# Function to get chatbot response
def get_response(user_query, chat_history):
    template = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request.

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

     # Using LM Studio Local Inference Server
    llm = ChatOpenAI(base_url="http://localhost:1234/v1", openai_api_key=openai_api_key, model="froggeric/WestLake-10.7B-v2-GGUF", temperature=temperature)

    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))

    