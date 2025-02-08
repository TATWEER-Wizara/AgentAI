from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()


# Configuration de la mémoire
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

company_name = "Croissant & Co",
previsions =  "Demande prévue : 1 500 croissants/jour pendant 3 jours (pic national).",
processes = [
    "Production/jour : 1 500 croissants (150kg de farine/jour).",
    "Stock initial de farine : 300kg (3 jours de production).",
    "Livraison prévue de farine : 150kg/jour (fournisseur A, contrat scanné PDF)."
],
constraints = [
    "2 fours en fonctionnement (capacité totale : 1 500 croissants/jour).",
    "Temps de cuisson : 15min par fournée (100 croissants/fournée).",
    "Fournisseur A : Livraison en 24h, coût = 1€/kg.",
    "Fournisseur B : Livraison en 12h, coût = 1.5€/kg (contrat d’urgence).",
    "Stockage max : 500kg de farine (limite du local).",
    "2 boulangers disponibles (peuvent travailler 2h supplémentaires en urgence)."
],
cost_breakdown = [
    "labor : 10€/h par boulanger (2 boulangers).",
    "materials : Farine : 1€/kg (fournisseur A), 1.5€/kg (fournisseur B).",
    "overhead : Électricité : 50€/jour, Location du local : 100€/jour."
],
current_daily_production = "1 500 croissants/jour.",
bottlenecks = [
    "Capacité des fours : 1 500 croissants/jour.",
    "Stockage de farine : 500kg max.",
    "Temps de travail des boulangers : 8h/jour (peut être étendu à 10h/jour en urgence)."
]
     
# Outil personnalisé pour l'analyse IBP
class IBPAnalysisTool(Tool):
    def __init__(self):
        super().__init__(
            name="IBP Analyzer",
            func=self._analyze,
            description="Analyse des risques et recommandations pour la planification intégrée"
        )

    def _analyze(self, inputs):
        # Intégration de règles métier spécifiques à l'Algérie
        algerian_constraints = {
            "taxes": "TVA 19%",
            "imports": "Restrictions sur les matériaux électroniques",
            "normes": "Certification IRCM obligatoire"
        }







        






        # Simplified prompt for Gemini
        template = """
        Contexte:
        L'entreprise {company_name}, opérant sur le marché algérien, envisage {previsions}.
        Les spécifications et contraintes de l'entreprise sont définies dans le suivant :
        - Processus : {processes}
        - Contraintes : {constraints}
        - Coûts : {cost_breakdown}
        - Production actuelle : {current_daily_production}
        - Goulots d'étranglement : {bottlenecks}

        Rôle:
        Tu es un expert en planification intégrée (IBP) et en gestion opérationnelle. Ton rôle est de prédire et d'analyser les risques potentiels liés à l'augmentation de production de 25% pour le Produit Alpha, et de déterminer, parmi toutes les options possibles, la décision optimale à recommander pour validation par le responsable. 

        Instructions:
        1. **Analyse des Données** : Utilise les informations fournies dans le JSON pour répondre aux questions suivantes :
        - Quelle est la production actuelle ? (voir 'current_daily_production')
        - Quels sont les coûts actuels de production ? (voir 'cost_breakdown')
        - Quels sont les goulots d'étranglement actuels ? (voir 'bottlenecks')
        2. **Prédiction des Risques** : Identifie les risques potentiels liés à l'augmentation de production de 25%. Par exemple :
        - **Production** : Risque de surcharge des fours, insuffisance du temps de maintenance, baisse de qualité.
        - **Logistique** : Risque de rupture de stock, délais de réapprovisionnement trop longs, capacité de stockage insuffisante.
        - **Finance** : Risque de dépassement budgétaire, coûts imprévus.
        3. **Proposition d’Actions Correctives** : Pour chaque risque identifié, propose des mesures concrètes et justifie leur efficacité.
        4. **Sélection de la Décision Optimale** : Analyse toutes les options et détermine celle offrant le meilleur compromis entre coût (en DZD), délai et minimisation des risques. Explique clairement ton choix.
        5. **Activation de la Chain-of-Thought (CoT)** : Avant de fournir ta réponse finale, décris ton raisonnement étape par étape afin de garantir que toutes les contraintes et processus ont été pris en compte.
        6. **Structure de la Réponse** : Organise ta réponse de manière claire et structurée avec des titres et des listes numérotées, par exemple :
        - Étape 1 : Analyse de la Production
        - Étape 2 : Analyse Logistique
        - Étape 3 : Analyse Financière
        - Étape 4 : Synthèse et Sélection de la Décision Optimale
        7. **Conclusion** : Résume la décision optimale globale à recommander pour validation, en précisant que cette recommandation devra être validée par le responsable avant toute mise en œuvre.

        Exemple de Réponse Attendue :
        - Étape 1 : Analyse de la Production
        - Production actuelle : 1 500 croissants/jour.
        - Goulots d'étranglement : Capacité des fours (1 500 croissants/jour), stockage de farine (500kg max).
        - Étape 2 : Analyse Logistique
        - Risque de rupture de stock si la demande dépasse 1 500 croissants/jour.
        - Solution : Commander de la farine supplémentaire auprès du fournisseur B (1.5€/kg) pour éviter les ruptures.
        - Étape 3 : Analyse Financière
        - Coût supplémentaire : 150kg/jour × 1.5€/kg = 225€/jour.
        - Budget disponible : 100 000€.
        - Conclusion : L'augmentation de production est réalisable dans le budget.
        - Étape 4 : Synthèse et Sélection de la Décision Optimale
        - Recommandation : Augmenter la production à 1 875 croissants/jour en utilisant le fournisseur B pour la farine supplémentaire.
        - Conclusion : Cette décision est recommandée pour validation par le responsable avec les calculs nécessaires afin de bien justifier la decision.
        """


        
        prompt = PromptTemplate(
            template=template,
            input_variables=["forecast", "process", "constraints"],
            partial_variables={"al_constraints": algerian_constraints}
        )
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)  
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(inputs)

# Initialisation de l'Agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)  
tools = [IBPAnalysisTool()]

agent = initialize_agent(
    tools = [],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Exemple d'utilisation
response = agent.run(
    f""" Contexte:
        L'entreprise {company_name}, opérant sur le marché algérien, envisage {previsions}.
        Les spécifications et contraintes de l'entreprise sont définies dans le suivant :
        - Processus : {processes}
        - Contraintes : {constraints}
        - Coûts : {cost_breakdown}
        - Production actuelle : {current_daily_production}
        - Goulots d'étranglement : {bottlenecks}

        Rôle:
        Tu es un expert en planification intégrée (IBP) et en gestion opérationnelle. Ton rôle est de prédire et d'analyser les risques potentiels liés à l'augmentation de production de 25% pour le Produit Alpha, et de déterminer, parmi toutes les options possibles, la décision optimale à recommander pour validation par le responsable. 
        Exemple de Réponse Attendue :
        - Étape 1 : Analyse de la Production
        - Production actuelle : 1 500 croissants/jour.
        - Goulots d'étranglement : Capacité des fours (1 500 croissants/jour), stockage de farine (500kg max).
        - Étape 2 : Analyse Logistique
        - Risque de rupture de stock si la demande dépasse 1 500 croissants/jour.
        - Solution : Commander de la farine supplémentaire auprès du fournisseur B (1.5€/kg) pour éviter les ruptures.
        - Étape 3 : Analyse Financière
        - Coût supplémentaire : 150kg/jour × 1.5€/kg = 225€/jour.
        - Budget disponible : 100 000€.
        - Conclusion : L'augmentation de production est réalisable dans le budget.
        - Étape 4 : Synthèse et Sélection de la Décision Optimale
        - Recommandation : Augmenter la production à 1 875 croissants/jour en utilisant le fournisseur B pour la farine supplémentaire.
        - Conclusion : Cette décision est recommandée pour validation par le responsable avec les calculs nécessaires afin de bien justifier la decision.
        """
)

print(response)