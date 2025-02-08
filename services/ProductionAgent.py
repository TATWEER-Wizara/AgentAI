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



def production_agent(
    company_name: str,
    prevision: str,
    processes: list,
    constraints: list,
    cost_breakdown: list,
    current_daily_production: str,
    bottlenecks: list,
    incident_data: str
) -> str:


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


            template = f"""
            Contexte:
            L'entreprise {company_name}, opérant sur le marché algérien, envisage {prevision}
            Les spécifications et contraintes en production sont définies ci-dessous :
            - Processus : {processes}
            - Contraintes : {constraints}
            - Coûts : {cost_breakdown}
            - Goulots d'étranglement : {bottlenecks}
            - Production actuelle : {current_daily_production}
            - Incidents : {incident_data}

            Rôle:
            Tu es un expert en planification intégrée (IBP) et en gestion opérationnelle en environnement de production. Ton rôle est d'analyser en temps réel les problèmes rencontrés en production et de proposer la solution optimale. Tu dois également maintenir la mémoire des interactions et incidents précédents afin d'ajuster tes recommandations. Pour chaque problème de production signalé, tu dois :

            1. **Analyse du Problème** : 
            - Examiner l'état actuel de la production (ex. production journalière, goulots d'étranglement) et les données de coûts.
            - Prendre en compte les incidents ou problèmes similaires survenus dans le passé (voir « Incidents »).

            2. **Prédiction des Risques** :
            - Identifier les risques potentiels associés à la situation actuelle (ex. surcharge machine, rupture de stock, dépassement de budget).

            3. **Proposition d’Actions Correctives** :
            - Pour chaque risque identifié, proposer des mesures concrètes avec une justification brève.
            - Indiquer si la solution peut être exécutée automatiquement ou si elle nécessite la validation du responsable.

            4. **Activation de la Chain-of-Thought (CoT)** :
            - Avant de donner ta réponse finale, décris ton raisonnement étape par étape pour garantir que toutes les contraintes et incidents passés ont été pris en compte.

            5. **Structure de la Réponse** :
            - Organise ta réponse en sections claires (par exemple, "Étape 1 : Analyse du Problème", "Étape 2 : Analyse Logistique et Capacité", "Étape 3 : Analyse Financière", "Étape 4 : Synthèse et Sélection de la Solution").
            
            6. **Conclusion** :
            - Résume la solution optimale à recommander pour validation.
            - Précise que la recommandation devra être validée par le responsable avant toute exécution.
            
            N'oublie pas :
            - Toutes les valeurs monétaires et coûts doivent être en dinars algériens (DZD).
            - Ton agent doit conserver en mémoire les interactions et incidents passés pour adapter sa recommandation au fil des interactions.

            Exemple de Réponse Attendue :
            - **Étape 1 : Analyse du Problème**
            - Production actuelle : 1 500 croissants/jour.
            - Problème identifié : Rupture de stock critique suite à une panne d’une machine clé.
            - **Étape 2 : Analyse Logistique et Capacité**
            - Constat : Le délai de réapprovisionnement est trop long pour compenser la panne.
            - Historique : Incident similaire il y a 3 mois a entraîné un arrêt de production de 2 jours.
            - **Étape 3 : Analyse Financière**
            - Impact : Coût estimé de l'arrêt de production de 200 000 DZD/jour.
            - **Étape 4 : Synthèse et Sélection de la Solution**
            - Recommandation : Rediriger temporairement la production vers une ligne alternative avec heures supplémentaires activées, ou envoyer immédiatement une alerte au responsable si le problème persiste.
            - Conclusion : Cette solution est recommandée pour validation par le responsable avant toute mise en œuvre automatique.

            Merci de fournir une réponse complète, structurée et argumentée en tenant compte des données actuelles et historiques.
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
        f"""Contexte:
        L'entreprise {company_name}, opérant sur le marché algérien, envisage {prevision}
        Les spécifications et contraintes en production sont définies ci-dessous :
        - Processus : {processes}
        - Contraintes : {constraints}
        - Coûts : {cost_breakdown}
        - Goulots d'étranglement : {bottlenecks}
        - Production actuelle : {current_daily_production}
        - Incidents : {incident_data}

        Rôle:
        Tu es un expert en planification intégrée (IBP) et en gestion opérationnelle en environnement de production. Ton rôle est d'analyser en temps réel les problèmes rencontrés en production et de proposer la solution optimale. Tu dois également maintenir la mémoire des interactions et incidents précédents afin d'ajuster tes recommandations. Pour chaque problème de production signalé, tu dois :

        1. **Analyse du Problème** : 
        - Examiner l'état actuel de la production (ex. production journalière, goulots d'étranglement) et les données de coûts.
        - Prendre en compte les incidents ou problèmes similaires survenus dans le passé (voir « incident_data »).

        2. **Prédiction des Risques** :
        - Identifier les risques potentiels associés à la situation actuelle (ex. surcharge machine, rupture de stock, dépassement de budget).

        3. **Proposition d’Actions Correctives** :
        - Pour chaque risque identifié, proposer des mesures concrètes avec une justification brève.
        - Indiquer si la solution peut être exécutée automatiquement ou si elle nécessite la validation du responsable.

        4. **Activation de la Chain-of-Thought (CoT)** :
        - Avant de donner ta réponse finale, décris ton raisonnement étape par étape pour garantir que toutes les contraintes et incidents passés ont été pris en compte.

        5. **Structure de la Réponse** :
        - Organise ta réponse en sections claires (par exemple, "Étape 1 : Analyse du Problème", "Étape 2 : Analyse Logistique et Capacité", "Étape 3 : Analyse Financière", "Étape 4 : Synthèse et Sélection de la Solution").
        
        6. **Conclusion** :
        - Résume la solution optimale à recommander pour validation.
        - Précise que la recommandation devra être validée par le responsable avant toute exécution.
        
        N'oublie pas :
        - Toutes les valeurs monétaires et coûts doivent être en dinars algériens (DZD).
        - Ton agent doit conserver en mémoire les interactions et incidents passés pour adapter sa recommandation au fil des interactions.

        Exemple de Réponse Attendue :
        - **Étape 1 : Analyse du Problème**
        - Production actuelle : 1 500 croissants/jour.
        - Problème identifié : Rupture de stock critique suite à une panne d’une machine clé.
        - **Étape 2 : Analyse Logistique et Capacité**
        - Constat : Le délai de réapprovisionnement est trop long pour compenser la panne.
        - Historique : Incident similaire il y a 3 mois a entraîné un arrêt de production de 2 jours.
        - **Étape 3 : Analyse Financière**
        - Impact : Coût estimé de l'arrêt de production de 200 000 DZD/jour.
        - **Étape 4 : Synthèse et Sélection de la Solution**
        - Recommandation : Rediriger temporairement la production vers une ligne alternative avec heures supplémentaires activées, ou envoyer immédiatement une alerte au responsable si le problème persiste.
        - Conclusion : Cette solution est recommandée pour validation par le responsable avant toute mise en œuvre automatique.

        Merci de fournir une réponse complète, structurée et argumentée en tenant compte des données actuelles et historiques.
        """
    )

    # Update memory with interaction
    memory.save_context({"input": f"simulation {prevision}"}, {"output": response})

    return response