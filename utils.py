import csv, os, pymongo

here = os.path.dirname(os.path.abspath(__file__))

def store_to_mongodb(database, collection, fields, data, drop_collection=False, mode = 'json'):
    '''
    database: Name of mongodb database
    collection: Name of mongodb collection
    fields: Names of fields
            [field1_name, field2_name, ..., fieldn_name]
    data: Field values stored in csv format
            [[field1_value1, field2_value1, ..., fieldn_value1]
            [field1_value2, field2_value2, ..., fieldn_value2],
            ...
            [field1_valuem, field2_valuem, ..., fieldn_valuem]]]
    '''
    docs = []
    for row in data:
        doc = {}
        for i in range(len(fields)):
            doc[fields[i]] = row[i]
        docs.append(doc)
    
    creds = "mongodb+srv://tecker:iXVXtgPpCDZi5XYZ@cluster0.2cxow.mongodb.net/kayla?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

    client = pymongo.MongoClient(creds, 27017)
    db = client.get_database(database)
    if drop_collection:
        db.drop_collection(collection)
    coll = db.get_collection(collection)
    coll.insert_many(docs)

    client.close()

def load_from_mongodb(database, collection, query, details={}):
    '''
    database: Name of mongodb database
    collection: Name of mongodb collection
    query: Query object
            {'field_name': 'field_value'}    
    -------
    returns pymongo.cursor.Cursor instance
    '''
    creds = "mongodb+srv://tecker:iXVXtgPpCDZi5XYZ@cluster0.2cxow.mongodb.net/kayla?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

    client = pymongo.MongoClient(creds, 27017)
    db = client.get_database(database)
    coll = db.get_collection(collection)

    result = coll.find(query, details)
    client.close()
    return result