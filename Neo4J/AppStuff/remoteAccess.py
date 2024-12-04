from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get credentials from environment variables
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Define a connection function


def connect_to_aura(uri, user, password):
    # Create the driver
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Define a query function
    def run_query(query, parameters=None):
        with driver.session() as session:
            result = session.run(query, parameters)
            return result.data()

    # Example query
    example_query = "MATCH (n) RETURN n LIMIT 5"
    results = run_query(example_query)

    # Print results
    print("Results:", results)

    # Close the driver
    driver.close()


# Connect to AuraDB
connect_to_aura(uri, username, password)
