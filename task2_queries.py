import os
import pymongo
from dotenv import load_dotenv
load_dotenv()


mongo_pass = os.getenv("mongo_pass")
client = pymongo.MongoClient(f"mongodb+srv://kushagra:{mongo_pass}@first-cluster.lhruc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['kushagra_soni']
collection = db["flipkart"]
print("Done establishing the connection.")

if __name__ == '__main__':
    # query #1
    number_of_products = collection.count_documents({})
    print("The number of products scraped =", number_of_products)

    # query #2
    discounted_products = 0
    all_products = collection.find({})
    for product in all_products:
        if product['original_price($)'] and product["sale_price($)"] and product['original_price($)'] < product["sale_price($)"]:
            discounted_products += 1
    print("Products with discounted price =", discounted_products)

    # query #3
    # topwear_no_discount = collection.find({
    #     "$and" : [{
    #             "product_category" : "topwear",
    #         },
    #         {
    #             "$eq" : {
    #                 "original_price($)" : "sale_price($)"
    #             }
    #         }
    #     ]
    # })
    topwear_no_discount = list(collection.aggregate([
        {
            '$project': {
                'diff': {'$subtract': ['$original_price($)', '$sale_price($)']},
                'sale_price($)': 1,
                'origial_price($)': 1,
                'product_category' : 1
            }
        },
        {
            '$match': [
                {'diff': {'$eq': 0}}
            ],
        }
    ]))
    print(type(topwear_no_discount), len(topwear_no_discount))
    print(topwear_no_discount[:5])