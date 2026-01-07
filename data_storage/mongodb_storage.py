from pymongo import MongoClient
import pandas as pd

class MongoStorage:
    """MongoDB for structured storage"""

    def __init__(self, uri, db_name):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            # Test connection
            self.client.server_info()
            print("MongoDB connected")
        except Exception as e:
            print(f"MongoDB not available: {e}")
            self.client = None
            self.db = None

    def store_documents(self, collection_name, documents):
        """Store documents in MongoDB"""
        if self.db is None:
            return

        try:
            collection = self.db[collection_name]
            if isinstance(documents, pd.DataFrame):
                documents = documents.to_dict('records')

            if documents:
                collection.insert_many(documents)
                print(f"Stored {len(documents)} documents in {collection_name}")
        except Exception as e:
            print(f"MongoDB error: {e}")