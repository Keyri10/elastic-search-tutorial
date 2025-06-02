from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/', methods=['GET', 'POST'])
def handle_search():
    query = request.form.get('query', '').strip()
    from_ = int(request.form.get('from_', 0))
    size = 10  # Número de resultados por página

    results = []
    total = 0
    aggs = {}

    if query:
        body = {
            "query": {
                "query_string": {
                    "query": query
                }
            },
            "from": from_,
            "size": size,
            "aggs": {
                "category": {
                    "terms": {
                        "field": "category.keyword"
                    }
                }
            }
        }
        res = es.search(index="movies", body=body)

        total = res['hits']['total']['value']
        results = res['hits']['hits']

        # Procesar agregaciones para pasarlas a la plantilla
        if 'aggregations' in res:
            aggs = {
                "Category": {bucket['key']: bucket['doc_count'] for bucket in res['aggregations']['category']['buckets']}
            }

    return render_template('index.html', query=query, results=results, total=total, from_=from_, aggs=aggs)

@app.route('/document/<id>')
def get_document(id):
    doc = es.get(index="movies", id=id, ignore=[404])
    if doc['found']:
        return doc['_source']
    else:
        return 'Document not found', 404

if __name__ == '__main__':
    app.run(debug=True)
