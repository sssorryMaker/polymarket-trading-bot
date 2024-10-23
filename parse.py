#Ollama allows the program to run open source llms locally
#Langchain allows the program to connect LLMs to the python code
#Must have Ollama installed
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#Instructions given to llm
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {extract_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.2:1b")

#creating a prompt template, using it for a model
def extract_with_ollama(dom_chunks, extract_description):
    prompt = ChatPromptTemplate.from_template(template)
    #chain means we will first go to the prompt and then call the model
    chain = prompt | model

    extracted_results = []

# Taking all the 6000 chracters chunks and passing them into the prompt
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "extract_description": extract_description})
        print(f"Extracted batch {i} of {len(dom_chunks)}")
        extracted_results.append(response)

    return "\n".join(extracted_results)