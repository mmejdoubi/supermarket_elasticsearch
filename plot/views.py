from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
from elasticsearch import Elasticsearch
from django.shortcuts import render_to_response
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
import json
import requests

def plot_income(request):

    query_json = {
        "aggregations": {
            "MARITAL_STATUS_CODE": {
                "terms": {
                    "field": "MARITAL_STATUS_CODE",
                    "size": 0
                },
                "aggregations": {
                    "ln": {
                        "terms": {
                            "field": "INCOME_DESC",
                            "size": 0
                        }
                    }
                }
            }
        } }

    es = Elasticsearch(host='localhost',port=9200)
    res = es.search(index="demographics", body=json.dumps(query_json))
#    res = requests.post('http://localhost:9200/demographics/_search',data=json.dumps(query_json)).text
#    res = json.loads(res)
    print res

    data = []

    for _count in res['aggregations']['MARITAL_STATUS_CODE']['buckets'][0]['ln']['buckets']:
        data.append([_count['key'], _count['doc_count']])

    data_source = SimpleDataSource(data= data)

    chart = BarChart(data_source)
    context = {'chart': chart}

    return render_to_response( 'plot.html', context)
