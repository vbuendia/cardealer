import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
   
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        #if kwargs["api_key"]:
        # Basic authentication GET
        #  response = requests.get(url, headers={'Content-Type': 'application/json'},
        #                             params=kwargs, auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        #else:
          # no authentication GET
          response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):

    print("POST to {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        #if kwargs["api_key"]:
         # Basic authentication GET
        #  response = requests.post(url, headers={'Content-Type': 'application/json'},
        #                            params=kwargs, auth=HTTPBasicAuth('apikey', kwargs["api_key"]), data=json.dumps(json_payload))
        #else:
         # no authentication POST
          response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, data=json.dumps(json_payload))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
     
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer #["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"],full_name=dealer_doc["full_name"])
            results.append(dealer_obj)

    return results


def get_dealer_by_dealerid(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId = dealerId)
    
    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer #["doc"]
            # Create a CarDealer object with values in `doc` object
            if dealer_doc["id"]==dealerId:
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"],full_name=dealer_doc["full_name"])
                return (dealer_obj)
    else:
        return "No dealer"
    return results

def get_dealer_by_state(url, stat):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state = stat)
    if json_result:
        # Get the row list in JSON as dealers
        
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer #["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"], full_name = dealer_doc["full_name"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealer_id)
    
    if json_result:
        # Get the row list in JSON as dealers
   
        reviews = json_result["body"]["data"]["docs"]
        
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(               
              name=review["name"],
              purchase=review["purchase"],
              review=review["review"],
              purchase_date=review["purchase_date"],
              car_make=review["car_make"],
              car_model=review["car_model"],
              car_year=review["car_year"],
              sentiment=analyze_review_sentiments(review["review"]),
              id=review["id"],
              dealership=review["dealership"])
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(texto):

   apikey = 'rg6Pp19-6x_1Rq1vPyXCK9v9VyvZnKsypHE8IfxrhQ_S'
   url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/9ea34d67-ddf9-4511-ad85-76cff823b461'
   texto_add = " hello hello hello"

   authenticator = IAMAuthenticator(apikey) 
   natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

   natural_language_understanding.set_service_url(url) 
   response = natural_language_understanding.analyze( text=texto+texto_add,features=Features(sentiment=SentimentOptions(targets=[texto+texto_add]))).get_result() 

   label=json.dumps(response, indent=2) 

   label = response['sentiment']['document']['label'] 

   return(label) 
   
