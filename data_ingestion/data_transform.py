import pandas as pd
from langchain_core.documents import Document

class data_converter:

    def __init__(self):
        self.product_data = pd.read_csv(r"D:\LLM_Project\data\amazon_product_review.csv")
        print(self.product_data.head())

    def data_transformation(self):
        pass



if __name__ == '__main__':
    data_conn = data_converter()