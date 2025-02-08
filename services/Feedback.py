from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()



# Set up conversation memory (stateful memory)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

# Define a prompt template for processing feedback
feedback_template = """
Contexte:
Ton rôle est de recevoir des retours sur ta solution de planification intégrée (IBP). 
Tu as déjà fourni une solution et maintenant tu reçois un feedback. 
Feedback reçu: {feedback}

Instructions:
- Lis le feedback.
- Ne génère aucune analyse détaillée.
- Réponds uniquement par une phrase courte indiquant que tu as bien noté le feedback, par exemple : "Noted, thanks for the feedback."
- Mets à jour ta mémoire avec ce feedback pour améliorer tes futures recommandations, sans réexécuter d'analyse.

Réponds uniquement par une phrase courte.
"""

# Create a PromptTemplate for the feedback loop
feedback_prompt = PromptTemplate(
    template=feedback_template,
    input_variables=["feedback"]
)

# Initialize your LLM (using Google's Gemini in this example)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)

# Create an LLMChain that will process the feedback
feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)

def process_feedback(feedback_text):
    # Process the feedback using the LLMChain
    response = feedback_chain.run({"feedback": feedback_text})
    
    # Update the memory with the feedback (storing both input and the received feedback)
    memory.save_context({"input": "Feedback received"}, {"output": feedback_text})
    
    return response

# Example usage:
feedback_input = "La solution semble correcte dans l'ensemble, mais ajuste les estimations de coûts de production."
feedback_response = process_feedback(feedback_input)
print("Feedback Response:")
print(feedback_response)