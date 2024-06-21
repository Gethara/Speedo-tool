import os
import streamlit as st
import pickle
import time
import magic
import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAI
#from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import faiss


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

st.title("Speedo: News Research Tool📚")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
llm = OpenAI(model_name="gpt-3.5-turbo",temperature=0.9, max_tokens=500)

#added later
class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

#added later
def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([para.get_text() for para in paragraphs])
            return text
        else:
            st.write(f"Failed to fetch {url}")
            return None
    except Exception as e:
        st.write(f"Error fetching or processing {url}, exception: {e}")
        return None

if process_url_clicked:
    # load data
    #loader = UnstructuredURLLoader(urls=urls)
    #main_placeholder.text("Data Loading  ◼◼◼◼◼◼")
    #data = loader.load()
    
# Fetch and parse data manually
    raw_data = []
    for url in urls:
        if url:
            content = fetch_and_parse_url(url)
            if content:
                raw_data.append(Document(page_content=content, metadata={"source": url}))
    
    # Debug: Check if raw data is fetched and parsed
    st.write(f"Fetched and parsed data from {len(raw_data)} URLs.")
    
    if not raw_data:
        st.error("No data loaded. Please check the URLs.")
      
    else:
    # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000,
            chunk_overlap=200
        ) 
        main_placeholder.text("Text Splitting ◼◼◼◼◼◼")
        docs = text_splitter.split_documents(raw_data)
        
        #added later
        st.write(f"Split into {len(docs)} chunks.")
        if not docs:
            st.error("No documents created after splitting. Please check the input data.")
        else:
            # Create embeddings and save it to FAISS index
            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
            main_placeholder.text("Embedding Vector Started Building...✅✅✅")
            time.sleep(2)
            
            # Save the FAISS index to a pickle file
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_openai, f)


query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)




