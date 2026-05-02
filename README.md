# ☁️ Project Sky-Graph: Global Cloud Infrastructure Mapper

Project Sky-Graph is an end-to-end serverless data pipeline and interactive geospatial dashboard. It acts as an open-source intelligence (OSINT) tool designed to dynamically map the hidden cloud infrastructure routing the internet. 

Currently configured to map the entire UK Higher Education sector, the pipeline resolves domains to IP addresses, queries geolocation and ISP data, and visualizes the physical data centers on a 3D interactive map.

## 🏗️ System Architecture

This project is built on a decoupled, scale-to-zero serverless architecture:

1. **Data Orchestration (Python):** A batch processor dynamically fetches target domains (via open APIs like hipolabs) and orchestrates the data flow.
2. **Microservice Engine (AWS Lambda & API Gateway):** A serverless Python function handles DNS resolution (`socket`) and external API requests (`urllib`) to gather ISP and geolocation coordinates, returning clean JSON.
3. **Data Transformation (Pandas):** Nested JSON responses are flattened and structured into tabular datasets.
4. **Visualization (Streamlit & PyDeck):** A deployed web application renders the intelligence data onto an interactive, 3D geospatial map.

## ✨ Key Features
* **Serverless Compute:** Utilizes AWS Lambda (FaaS) for highly scalable, zero-maintenance execution.
* **API Orchestration:** Dynamically aggregates data from multiple distinct REST APIs.
* **Resilient Error Handling:** Built-in fault tolerance for dead domains, DNS resolution failures, and 400/500 HTTP errors.
* **Automated Rate Limiting:** Algorithmic pacing to respect third-party API limits and prevent IP bans.
* **Geospatial Rendering:** Utilizes Uber's Deck.GL (via PyDeck) for high-performance 3D mapping and interactive HTML tooltips.

## 🛠️ Tech Stack
* **Cloud Infrastructure:** AWS Lambda, Amazon API Gateway, IAM
* **Backend:** Python 3.12, `socket`, `urllib`, `requests`
* **Data Engineering:** Pandas, JSON
* **Frontend UI/UX:** Streamlit, PyDeck
* **Deployment:** Streamlit Community Cloud, Git/GitHub

## 🚀 Quick Start (Local Development)

### Prerequisites
* Python 3.9+
* An active AWS account (to deploy the Lambda function)

### 1. Set up the environment
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/entoeco/cloud-compute-mapper.git](https://github.com/entoeco/cloud-compute-mapper.git)
cd cloud-compute-mapper
pip install -r requirements.txt
