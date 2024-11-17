DOCIR: A Python Project for Information Retrieval from Diverse Data Sources
DOCIR (Document Information Retrieval) is a robust Python-based solution designed to extract, process, and analyze information from various unstructured data sources such as PDFs, HTML files, emails, and CSV files. Leveraging state-of-the-art AI models and graph database technology, DOCIR provides a comprehensive framework for retrieving and understanding data at scale.

Features
Unstructured Data Handling: Efficient chunking of PDFs, HTML, emails, and CSV files using the unstructured I/O library.
Graph-Based Storage: Utilizes Neo4j for storing and querying relationships and dependencies in the data.
Advanced Embeddings:
LLaMA for general-purpose embeddings.
BGerRanker for ranking and prioritizing retrieved data.
Nomadic Embedding Models for handling domain-specific retrieval tasks.
Query Flexibility: Natural language querying and retrieval capabilities.
Scalable Architecture: Built to handle large datasets with modular and extensible components.
Installation
Prerequisites
Ensure you have the following installed on your system:

Python 3.8 or later
Neo4j (Community or Enterprise Edition)
Required Python libraries (see below)
Step-by-Step Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-repo/docir.git
cd docir
Set Up Python Environment:

bash
Copy code
python3 -m venv env
source env/bin/activate  # For Linux/MacOS
env\Scripts\activate     # For Windows
Install Dependencies: Install required Python packages using:

bash
Copy code
pip install -r requirements.txt
Configure Neo4j:

Install and run Neo4j locally or on a server.
Configure the connection details (e.g., URI, username, password) in the project's .env file.
Run the Application:

bash
Copy code
python app.py
Usage
1. Input Sources
DOCIR accepts the following input formats:

PDF: Extract text and metadata.
HTML: Parse content and structure.
Emails: Analyze email headers, body, and attachments.
CSV: Process tabular data.
2. Chunking and Preprocessing
Data is chunked into manageable pieces using the unstructured library to facilitate efficient processing and retrieval.

3. Embedding Models
Choose between LLaMA, BGerRanker, and Nomadic models based on your use case.
Generate embeddings to encode textual or tabular information for semantic retrieval.
4. Graph Database Integration
Data is ingested into Neo4j, where relationships and dependencies can be explored using Cypher queries.
5. Query and Retrieval
Natural language queries can be made to retrieve information.
Results are ranked and filtered using advanced ranking models.
