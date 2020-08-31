#search log for py
from flask import Flask , request, make_response, jsonify
from elasticsearch import Elasticsearch
app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!'#function for responses

#function for responses
def results():
  # build a request object
  req = request.get_json(force=True)
  #fetch action from json
  action = req.get('queryResult').get('action')
  if action == 'searchByInterfaceId':
    res = search_ByinterfaceId(req)
  elif action == 'searchByErrorCode':
    res = search_ByErrorCode(req)
  
  #action = 'Hi, I just wanted to check'
  #return a fulfillment response
  return {'fulfillmentText': res}

def search_ByinterfaceId(req):
  user_request= req.get('interfaceId')
  query_body = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "INTERFACE_ID": user_request
        }
      }
    }
  }
}
  elastic_client = Elasticsearch(hosts=["https://ed9ad1fdba634fa1b1c423c5c60ad580.asia-south1.gcp.elastic-cloud.com"])
  result = elastic_client.search(index="ms-elastic-search-logs", body=query_body)
  return(printallHits(result))
def search_ByErrorCode(req):
  user_request= req.get('errorCode')
  query_body = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "ERROR_CODE": user_request
        }
      }
    }
  }
}
  elastic_client = Elasticsearch(hosts=["https://ed9ad1fdba634fa1b1c423c5c60ad580.asia-south1.gcp.elastic-cloud.com"])
  result = elastic_client.search(index="ms-elastic-search-logs", body=query_body)
  return(printallHits(result))
def printallHits(result):
 all_hits = result['hits']['hits']
 data = ''
 for num, doc in enumerate(all_hits):
    print ("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")

    # Use 'iteritems()` instead of 'items()' if using Python 2
    for key, value in doc.items():
    
        print (key, "-->", value)
        data = data +value
    # print a few spaces between each doc for readability
    print ("\n\n")

    return data

    #create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  # return response
  return make_response(jsonify(results()))#run the app
if __name__ == '__main__':
  app.run(port=8000,debug=True)
