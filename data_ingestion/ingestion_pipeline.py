import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_astradb import AstraDBVectorStore
from utils.model_loader import ModelLoader
from config.config_loader import load_config

class DataIngestion:
    ## This class takes care of data ingestion and transformation into AstraDB vectore store.

    #Initialize enviroment variables, embedding model and set the CSV file path
    def __init__(self):
        print("Initializing Data Ingestion Pipeline---")
        self.model_loader= ModelLoader()
        self._load_env_variables()
        self.csv_path = self._get_csv_path()
        self.product_data = self._load_csv()
        self.config = load_config()

    #Load and validate required environment variables
    def _load_env_variables(self):
        load_dotenv()
        req_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        missing_vars = [var for var in req_vars if os.getenv(var) is None]
        if missing_vars:
            raise EncodingWarning(f"missing environment variables: {missing_vars}")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace=os.getenv("ASTRA_DB_KEYSPACE")

    #get the path of the csv file located in the data folder
    def _get_csv_path(self):
        current_dir = os.getcwd()
        csv_path = os.path.join(current_dir, 'data', 'amazon_product_review.csv')

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"csv file not found in: {csv_path}")
        
        return csv_path
    
    #load data from csv
    def _load_csv(self):
        df = pd.read_csv(self.csv_path)
        expected_columns = {'product_title', 'rating', 'summary', 'review'}

        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV is expected to have colums: {expected_columns}")
    
        return df
    
    #transform product data into list of Langchain Document objects

    def transform_data(self):
        product_list = []

        for index, row in self.product_data.iterrows():
            object={
                "product_name":row['product_title'],
                "product_rating":row['rating'],
                "product_summary": row['summary'],
                "product_review": row['review']
            }

            product_list.append(object)
        #print("************printing product list*************")
        #print(product_list[0])

        ## Store product list in a vector DB(ASTRA DB)
        documents = []
        for entry in product_list:
            metadata = {
                "product_name": entry["product_name"], 
                "product_rating": entry["product_rating"],
                "product_summary": entry["product_summary"]
            }
            doc = Document(page_content=entry["product_review"], metadata=metadata)
            documents.append(doc)

        print(f"Transformed {len(documents)} documents.")
        return documents
    
    #store document into AStraDB vectore store.
    def store_in_vector_db(self, documents: List[Document]):
        collection_name = self.config["astra_db"]["collection_name"]
        vstore = AstraDBVectorStore(
            embedding=self.model_loader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.db_api_endpoint,
            token=self.db_application_token,
            namespace=self.db_keyspace,
        )

        inserted_ids = vstore.add_documents(documents)
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids

    
    #Run data ingestion pipeline: transform data and store transformed data into the vector DB
    def run_pipeline(self):
        documents = self.transform_data()
        vstore, inserted_ids = self.store_in_vector_db(documents)

        # optionally do a quicl search
        query = "Can you give the lowest budge headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample seaerch results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run_pipeline()