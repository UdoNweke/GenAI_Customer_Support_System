import pandas as pd
from langchain_core.documents import Document

class data_converter:

    def __init__(self):
        self.product_data = pd.read_csv(r"D:\LLM_Project\data\amazon_product_review.csv")
        #print(self.product_data.head())

    def data_transformation(self):
        data_colums = self.product_data.columns
        data_colums =list(data_colums[1:])
        #print(data_colums)

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
        docs = []
        for entry in product_list:
            metadata = {"product_name": entry["product_name"], "product_rating": entry["product_rating"], "product_summary": entry["product_summary"]}
            doc = Document(page_content=entry["product_review"], metadata=metadata)
            docs.append(doc)

        #print(docs[0])
        return docs





if __name__ == '__main__':
    data_conn = data_converter()
    data_conn.data_transformation()