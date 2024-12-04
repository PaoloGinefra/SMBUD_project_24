from flask import Flask, jsonify
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get credentials from environment variables
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Create a Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define a route to fetch data from Neo4j


@app.route("/api/neo4j-data", methods=["GET"])
def get_neo4j_data():
    try:
        # Create a session and run a query
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 5")
            data = [record['n'] for record in result.data()]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
