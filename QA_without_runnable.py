# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI


template = """Extract the answer to the following question from the provided text and format it in JSON. Ensure the response is concise, accurate, and specific to the details mentioned in the text.

Question: {question}

Text: ```{context}```


Guidelines:
- Provide only the answer, formatted as JSON. Do not include the question in the answer.
- If the information is not explicitly mentioned in the text, respond with: "not available".
- Avoid adding context, explanations, or assumptions. Only use the provided text as the source.
- Keep the answer brief and exact.
"""


prompt = ChatPromptTemplate.from_template(template)


def get_text_chunks_langchain(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_question_answers(texts, question, openai_api_key):
    data_dict = {}
    count = 0

    docs = get_text_chunks_langchain(texts)
    # print(len(docs))
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Storing embeddings in the vector store
    vectorstore = FAISS.from_documents(docs, embeddings)

    model = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=openai_api_key)#"gpt-4-turbo" gpt-3.5-turbo

    # create a chain to answer questions
    qa = RetrievalQA.from_chain_type(
        llm=model, chain_type="stuff", retriever=vectorstore.as_retriever(), return_source_documents=True)

    # for question in list_questions:

    result = qa.invoke({"query": question})
    # print(result['result'])
    # context_query_gpt.append(result['source_documents'])

    return result['result']








