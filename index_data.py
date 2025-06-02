from elasticsearch import Elasticsearch
import json

# Conexión a Elasticsearch (versión 8.x cliente y servidor)
es = Elasticsearch("http://localhost:9200")

# Leer el archivo data.json
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)

# Indexar los documentos
for i, doc in enumerate(data):
    es.index(index="movies", id=i+1, document=doc)

print("Datos indexados correctamente.")
