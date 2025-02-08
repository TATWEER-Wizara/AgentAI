<p align="center">
  <img src="https://res.cloudinary.com/djn5zzqou/image/upload/v1739042857/TATWEER/ANALEASE.png" height="75" alt="ANALEASE Logo" />
  <img width="0" />
  <img width="0" />
  <img src="https://skillicons.dev/icons?i=fastapi" height="75" alt="FastAPI Logo" />
</p>

# Wazir Agent - Integrated Business Planning (IBP) Agent

**Wazir Agent** is an AI-driven solution that leverages a LangChain-based agent to predict risks related to production planning and recommend optimal decisions in a production environment. The application includes three main endpoints:

- `/simulation-agent`: Simulates risk analysis and decision recommendations based on static IBP inputs.
- `/production-agent`: Processes real-time production issues and provides an optimal solution while maintaining state (memory).
- `/feedback`: Accepts feedback from the production process, and save it to the agent's memory for future.

The solution is designed to work in the Algerian market, with all monetary values converted to dinars algériens (DZD).

---

## Features

- **Multi-Step Reasoning & Risk Prediction**  
  Leverages an LLM with a Chain-of-Thought prompt to analyze production data (processes, constraints, cost breakdown, current production, bottlenecks, incidents) and predict potential risks.

- **Stateful Production Agent**  
  Maintains conversation state (using ConversationBufferMemory) to store past interactions and incident data, ensuring refined recommendations across multiple interactions.

- **Feedback Loop with Dynamic Tool Calling**  
  Processes feedback by analyzing if the solution is accepted or rejected. 

- **Flexible and Modular Architecture**  
  Built with FastAPI and LangChain, allowing for easy integration, extension, and deployment in various environments.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)


---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/wizara-agent.git
   ```
2. **Navigate to the project directory**:

    ```bash
    cd wizara-agent
    ```


## Installing Dependencies

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Setting Up Environment Variables

1. **Create a `.env` file** in the `root` directory with the following structure:

    ```plaintext
    GOOGLE_API_KEY=
    ```


2. **Explanation of Environment Variables**:
`GOOGLE_API_KEY`: The API key of the LLM  that powers the LangChain Agent

## Running the application
Simply run the following command

```bash
uvicorn server:app
```
 

## API Documentation

   After running the server, you can use the Swagger integrated documentation to test the available endpoints. The Swagger documentation provides a detailed overview of all the requests you can make to interact with the API.

   - You can find the Swagger documentation for this project at `http://127.0.0.1:8000/docs/`

   Make sure the server is running at `http://127.0.0.1:8000` before testing the endpoints.


## Contact

For inquiries or feedback, reach out to us at:

- 📧 Email: [ma_fellahi@esi.dz](mailto:ma_fellahi@esi.dz), 
- 🌐 WhatsApp: +213 551 61 19 83
- **GitHub :** [flh-raouf](https://github.com/flh-raouf) , 
