from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:KDHNemuJIrzrEiENrdwZWtcZ:e5e8a4556f5642c4a2f68a9550ac9d52571d395b4a26287b658fcc5a512ebe1e")

# Correct way to get the database (keyspace) object
db = client.get_database_by_api_endpoint(
    "https://a01bdfbf-2242-4ccb-8073-418f50d1cfba-us-east-2.apps.astra.datastax.com"
)


# List collection names (note the absence of `.mercadolivre`)
print(f"Connected to Astra DB: {db.list_collection_names()}") 