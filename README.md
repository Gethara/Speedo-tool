**Speedo: Research Tool (My First NLP Project!)**

This project, speedo (speed research extraction & document object), is a research tool built using Streamlit. It's my first foray into Natural Language Processing (NLP) and Large Language Models (LLMs), allowing me to explore information retrieval and question answering from multiple web sources.



**Features**

*   Takes multiple **URLs** as input.
*   Loads and processes the content of those **URLs** with a focus on speed.
*   Splits the text content into smaller chunks for efficient processing.
*   Generates embeddings for the processed text using **OpenAI embeddings**.
*   Allows users to ask questions based on the provided URLs.
*   Retrieves answers and sources using a **RetrievalQAWithSourcesChain** from Langchain.



  
  **Getting Started**

1.  Clone the repository:

    `git clone https://github.com/gethara/speedo-tool.git`

 
2.   Install dependencies:

Navigate to the project directory and run:

    `pip install -r requirements.txt'


 3.   Edit .env

Enter your openai API key in .env file:

      `OPENAI_API_KEY=your_openai_api_key`


4. Run the application:

Start the Streamlit app by running:

      `streamlit run main.py`






 **Usage**

1. Open your web browser and navigate to http://localhost:8501.

2. Enter up to three URLs in the designated text boxes on the sidebar.

3. Click the "Process URLs" button. The application will load and process the provided URLs, displaying progress indicators.

4. Once processing is complete, a text box will appear for you to enter your question.

5. Click the "Submit" button to retrieve an answer and any relevant sources based on the processed text.







 **Technical Details**



*  **Frontend:** Streamlit

*   **Document Loading:** UnstructuredURLLoader (Langchain Community)

*  **Text Splitting:** RecursiveCharacterTextSplitter (Langchain)

*   **Embeddings:** OpenAIEmbeddings (Langchain OpenAI
*   **Vector Store:** Chroma (Langchain Chroma)


*   **Question Answering:** RetrievalQAWithSourcesChain (Langchain


*   **OpenAI API:** langchain_openai



  **Error Handling**

The application includes basic error handling for invalid URLs and unexpected exceptions. Specific error messages will be displayed in the Streamlit interface to guide the user.



**Disclaimer**

This research tool was created as my first NLP project and might not always provide accurate or complete information. It's recommended to use the retrieved answers as a starting point for further research and verification.
