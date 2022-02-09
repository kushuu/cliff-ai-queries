# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# python library to deal with mongoDB.
import pymongo

import os
from dotenv import load_dotenv   # library to load password from environment variables.
load_dotenv()


class NetAPorterPipeline:

    def __init__(self):
        '''
        initializer of pipeline object. This has all the required variables to establish a connection to mongoDB.
        '''
        mongo_pass = os.getenv("mongo_pass")  # fetching the mongodb password from environment variables file. This file is usually included in the .gitignore file.
        self.connection = pymongo.MongoClient(f"mongodb+srv://kushagra:{mongo_pass}@first-cluster.lhruc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.connection["kushagra_soni"]
        self.collection = self.db['flipkart']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
