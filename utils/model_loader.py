import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from config.config_loader import load_config

#Create a utility class to load embedding  and LLm models
class ModelLoader:

    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()

    #validate necessary environment variables
    def _validate_env(sef):
        req_var = ["GOOGLE_API_KEY"]
        missing_vars = [var for var in req_var if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
    #load and return enbedding model
    def load_embeddings(self):
        print("Loading embedding model")
        model_name = self.config["embedding_model"]["model_name"]
        return GoogleGenerativeAIEmbeddings(model= model_name)
    
    #load and return llm model
    def load_llm(self):
        print("Loading LLM")
        model_name=self.config["llm"]["model_name"]
        gemini_model = ChatGoogleGenerativeAI(model=model_name)

        return gemini_model
