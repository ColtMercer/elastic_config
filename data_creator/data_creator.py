from pymongo import MongoClient, collection
from elasticsearch import Elasticsearch
import os
import json
from time import sleep


def populate_mongodb() -> None:
    ''' Collects the contents of all the files in the data directory and saves them to MongoDB
    Args:
        None
    '''
    # colelct file contents and save to mongodb
    for dirpath, dirnames, filenames in os.walk('data'):
        for filename in filenames:
            # Collect Title and Year from filename
            # Example File Name: "1974 - Carrie.txt"
            year = int(filename[:4])
            title = filename[7:-4]
            print(f"Year: {year}, Title: {title}")

            # Read file contents
            with open(os.path.join(dirpath, filename), 'r') as file:
                contents = file.read()
            
            # Create a dictionary to save to MongoDB
            book = {
                'author': 'Stephen King',
                'year': year,
                'title': title,
                'contents': contents
            }

            # Save to MongoDB
            client = MongoClient(host=os.environ['MONGO_HOST'],
                                 port=27017,
                                 username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                                 password=os.environ['MONGO_INITDB_ROOT_PASSWORD'])
            db = client['books']
            collection = db['stephen_king']
            collection.insert_one(book)
            client.close()
            print(f"Saved {title} to MongoDB")

    print("Data Collection Complete")


def get_mongodb_collection() -> collection.Collection:
    ''' Returns the MongoDB collection
    Args:
        None
    Returns:
        pymongo.collection.Collection: MongoDB collection
    '''
    client = MongoClient(host=os.environ['MONGO_HOST'],
                        port=27017,
                        username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                        password=os.environ['MONGO_INITDB_ROOT_PASSWORD'])
    db = client['books']
    collection = db['stephen_king']
    return collection


def index_elasticsearch() -> None:
    ''' Index all books to Elasticsearch
    Args:
        None
    '''
    # Index all books to Elasticsearch
    elastic_url = 'http://es01:9200'
    elastic_user = 'elastic'
    elastic_password = 'changeme'
    client = Elasticsearch(
        [elastic_url],
        basic_auth=(elastic_user, elastic_password)
        )
    client.indices.create(index='stephen_king', ignore=400)

    collection = get_mongodb_collection()

    for book in collection.find():
        book = {
            "author": book['author'],
            "year": book['year'],
            "title": book['title'],
            "contents": book['contents']
        }
        client.index(index='stephen_king', body=book)
        print(f"Indexed {book['title']} to Elasticsearch")

    print("Indexing Complete")


if __name__ == '__main__':
    populate_mongodb()
    index_elasticsearch()
    sleep(360) # Give time to run a exec command