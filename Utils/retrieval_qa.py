from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub

def ask_with_rag(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=3)
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={"temperature": 0.5, "max_length": 512}
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain.run(input_documents=docs, question=query)
