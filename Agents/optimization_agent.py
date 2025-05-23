from retrieval_qa import ask_with_rag  # assuming you have a working RAG function

def optimization_agent(uploaded_pdf, query):
    if uploaded_pdf is None:
        return "Please upload a PDF document for optimization queries."

    if not query:
        return "Please enter a question to ask."

    # Call the RAG function
    response = ask_with_rag(uploaded_pdf, query)

    return response
