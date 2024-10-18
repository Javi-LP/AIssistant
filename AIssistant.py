from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI


OPENAI_KEY = "YOUR OPENAI KEY HERE"
DB_FAISS_PATH = 'vectorstore/db_faiss'
demo_prompt_template = 'Eres el asistente robot de MINOMBRE. Estas diseñado para responder preguntas sobre' \
                       'su vida laboral y personal.' \
                       'Nunca hagas preguntas. Ten en cuenta que debes proporcionar informacion.' \
                       'Si la pregunta no es una pregunta, reorientala hacia un contexto conocido.' \
                       'Aunque si la pregunta es un saludo, saluda amablemente y di que estas ahi para ayudar.' \
                       'Usa el contexto proporcionado para generar una contestacion fluida a la pregunta de forma ' \
                       'breve pero precisa.' \
                       'No seas repetitivo ni evasivo.' \
                       'Contexto: {context}' \
                       'Pregunta: {question}'

DATA_PATH = 'demodataPDFs/' #AQUI TUS DOCUMENTOS CON INFORMACION CONTEXTUAL

# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

#Loading the model
def load_llm():
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.9, api_key= OPENAI_KEY)
    return llm

#LLMChain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 10}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt})
    return qa_chain

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    qa_prompt = PromptTemplate(template=demo_prompt_template, input_variables=["context", "question"])
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

def init():
    create_vector_db()
    llm_chain = qa_bot()
    return llm_chain
