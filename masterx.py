from pymongo import ASCENDING, DESCENDING
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Connecting to MongoDB
uri = "mongodb+srv://kaushalrai:drS74VSLQl1KjRlW@cluster0.s9qlpue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
client.admin.command('ping')
print("Conectado a MongoDB!")
db = client.MIT588
collection = db.sensor
pipeline = [
        {
            '$group': {
                '_id': '$location',  # Group by the 'category' field
                'Humedad': {'$avg': '$humedad'}
            }
        }
    ]

@app.route('/')
def index():
    # Retrieve documents from MongoDB
    results = []

    documents = collection.aggregate(pipeline)
    print(type(documents))
    print('before results')
    for documento in documents:
        if documento['_id'] is None:
            print('NULL')
        else:
            print(type(documento))
            if documento['Humedad'] is not None:
                documento['Humedad'] = round(documento['Humedad'], 5)
            else:
                documento['Humedad'] = 0
            results.append(documento)

    datos = sorted(results, key=lambda x: x['_id'])
    datos2 = datos


    return render_template('charts.html', datos=datos, datos2=datos2)

if __name__ == '__main__':
    app.run(debug=True)


