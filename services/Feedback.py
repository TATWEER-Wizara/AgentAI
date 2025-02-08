import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

# Global memory instance to store conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

def feedback_agent(
    feedback: str,
    prevision: str,
    processes: list,
    constraints: list,
) -> str:
    
    # Create a prompt template that embeds all company-specific variables.
    prompt_template = f"""
        Contexte:
        L'entreprise envisage {prevision}
        Processus: {processes}
        Contraintes: {constraints}


        Feedback reçu: {feedback}

        Rôle:
        Tu es un expert en planification intégrée (IBP) et en gestion opérationnelle. Ton rôle est de recevoir des retours sur ta solution et d'analyser ce feedback.
        Si le feedback indique que la solution est acceptée, tu dois renvoyer une action d'appel d'outil sous forme de JSON pour appeler l'outil "SendEmailToManager" avec les paramètres suivants:
        - subject: "Production Solution Approved"
        - body: "The production solution has been approved based on the recent feedback: {{feedback}}. Please review the solution details for further action."
        Sinon, réponds simplement par "Noted, thanks for the feedback".

        Instructions:
        1. Active ta réflexion (Chain-of-Thought) pour déterminer si le feedback est positif ou négatif.
        2. Si positif, renvoie une action d'appel d'outil (en JSON) pour "SendEmailToManager" avec les clés 'subject' et 'body' comme indiqué.
        3. Sinon, répond simplement par "Noted, thanks for the feedback".
        4. Ne fournis aucune analyse détaillée dans ta réponse finale.

        Réponds uniquement par ta réponse finale ou par un appel à outil si nécessaire.
        """
    
    # Create a PromptTemplate using the above template; only "feedback" remains dynamic.
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["feedback"]
    )
    
    # Initialize the LLM (using Google's Gemini in this example)
    llm_instance = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    
    # Create an LLMChain with the prompt
    chain = LLMChain(llm=llm_instance, prompt=prompt)
    
    # Process the feedback using the chain
    response = chain.run({"feedback": feedback})

    # Update memory with interaction
    memory.save_context({"input": "feedback"}, {"output": feedback})
    
    return response