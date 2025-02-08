
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

from services.Feedback import feedback_agent
from services.SimulationAgent import simulation_agent
from services.ProductionAgent import production_agent


app = FastAPI()


class SimulationAgentRequest(BaseModel):
    prevision: str
    processes: List[str]
    constraints: List[str]
    incident_data: str

class ProductionAgentRequest(BaseModel):
    prevision: str
    processes: List[str]
    constraints: List[str]
    incident_data: str
    probleme: str

class FeedbackRequest(BaseModel):
    feedback: str
    prevision: str
    processes: List[str]
    constraints: List[str]



@app.post("/simulation-agent")
async def simulation_agent_main(request: SimulationAgentRequest):
    return simulation_agent(request)
    


@app.post("/production-agent")
async def production_agent_main(request: ProductionAgentRequest):
    return production_agent(request)
     

@app.post("/feedback")
async def feedback_main(request: FeedbackRequest):
    if (request["feedback"] == 'rejected'):
        return production_agent(request)
    return feedback_agent(request)
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



# company_name = "Croissant & Co"
# previsions = "Demande prévue : 1 500 croissants/jour pendant 3 jours (pic national)."
# processes = [
#     "Production/jour : 1 500 croissants (150kg de farine/jour).",
#     "Stock initial de farine : 300kg (3 jours de production).",
#     "Livraison prévue de farine : 150kg/jour (fournisseur A, contrat scanné PDF)."
# ]
# constraints = [
#     "2 fours en fonctionnement (capacité totale : 1 500 croissants/jour).",
#     "Temps de cuisson : 15min par fournée (100 croissants/fournée).",
#     "Fournisseur A : Livraison en 24h, coût = 1€/kg.",
#     "Fournisseur B : Livraison en 12h, coût = 1.5€/kg (contrat d’urgence).",
#     "Stockage max : 500kg de farine (limite du local).",
#     "2 boulangers disponibles (peuvent travailler 2h supplémentaires en urgence)."
# ]
# cost_breakdown = [
#     "labor : 10€/h par boulanger (2 boulangers).",
#     "materials : Farine : 1€/kg (fournisseur A), 1.5€/kg (fournisseur B).",
#     "overhead : Électricité : 50€/jour, Location du local : 100€/jour."
# ]
# current_daily_production = "1 500 croissants/jour."
# bottlenecks = [
#     "Capacité des fours : 1 500 croissants/jour.",
#     "Stockage de farine : 500kg max.",
#     "Temps de travail des boulangers : 8h/jour (peut être étendu à 10h/jour en urgence)."
# ]
# incident_data = "Incident 1 : Panne du four principal, Incident"