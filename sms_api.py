import json
import requests
from requests.auth import HTTPDigestAuth
from base64 import b64encode
from requests.auth import HTTPBasicAuth

from googleapiclient.discovery import build
import pprint


# 1) Search for a number having a pattern say 234208 using searching api
search_api_key = "https://api.plivo.com/v1/Account/MAY2MZMZUXNTYWMJY5MD/15402531895/"

def PlivoSearchApi(search_term, api_key, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, **kwargs).execute()
    return res['items']

results = PlivoSearchApi(
    '15402531895', search_api_key, num=10)
for result in results:
    pprint.pprint(result)

#3) send an sms from a number to another number.
class PlivoMsgApi(object):

    def __init__(self, auth_id, auth_token,api_id):
        self.has_authed = False
        self.auth_id = auth_id
        self.api_id = api_id
        self.auth_token = auth_token
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'

    def auth(self):

        if self.has_authed == False:
            self.auth()

        url = 'https://api.plivo.com/v1'

        response = requests.get(url,auth=HTTPDigestAuth(self.auth_id,self.auth_token), verify=True)
        if (response.ok):
            json_data = json.loads(response.content)

            print("Total iteam in response {0} properties".format(len(json_data)))
            
            for key in json_data:
                print(key + " : " + json_data[key])
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    #send message method takes
    #source, destination, text data as mandatory parameter
    def send_message(self,src,dst,text):
    	"""
    	@Author: Praveen
    	Date: 17/10/2017
    	src: 
    	dst:
    	text:
    	Function will send sms from one number to another,and take src, dst, text data as mandatory
    	"""
        url = 'https://api.plivo.com/v1/Account/{0}/Message/'.format(self.auth_id)

        params = {
            'src':src,
            'dst':dst,
            'text':text,
            'method':'POST'
        }

        #cash_credit is needed to verify the amount present in account
        url_account = 'https://api.plivo.com/v1/Account/{}/'.format(self.auth_id)
        response_data = requests.get(url_account, auth = (self.auth_id,self.auth_token))
        json_data = json.loads(response_data.text)
        cash_credit = json_data['cash_credits']

        response =requests.post(url, json=params, auth=(self.auth_id, self.auth_token))

        if (response.ok):
            json_data = json.loads(response.content)
            #self.verify_transaction_account(cash_credit,json_data['message_uuid'])
            print("The response contains {0} properties".format(len(json_data)))
            
            print(json_data)
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

auth_id = 'MAY2MZMZUXNTYWMJY5MD'
auth_token ='ZjMzMzBmYmZmZWZiOGJhODdmM2NmZjM0Yjg3YmUx'
api_id = 'https://api.plivo.com/v1'
x = PlivoMsgApi(auth_id, auth_token,api_id)
x.send_message(src='+15402531895',dst='+17853290976',text='hello plivo Team. This is praveen.')