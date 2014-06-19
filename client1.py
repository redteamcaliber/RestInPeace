'''
This is a simple client to invoke any of the REST API methods which can be invoked by an authenticated user. Make sure you enter a valid sessionIDand CSRF_TOKEN in the file named config before using this, else it will fail :). CSRF_TOKEN is just an antiCSRF token that is sent as a header. If
you don't need it, edit the code accordingly :).

If you want to invoke any of these without a session, edit the methods_authuser file and change 'Y' at the end of any line to 'N'

If you do not want to study traffic that is sent by the client, edit the code to communicate directly with the server by removing the "proxies" part from the invokeAPI method. If you DO pass traffic through Burp, ensure that you have the SUN JDK configured and not OpenJDK :)
'''

import sys
import base64
import requests

method_number_map = {}

def main():
  #Get all the APIs and the parameters that need to be sent with it
  all_methods = getAPIData()

  #Get sessionID and antiforgery token needed to invoke methods
  sessId, antiforgerytoken = read_config_file()

  #Menu driven option which lets the user choose which API to invoke
  method_number_to_invoke = chooseAPI(all_methods)

  #Actually invoke the API
  invokeAPI(all_methods, method_number_to_invoke)

def read_config_file():
  global antiforgerytoken
  global sessId

  f=open('config','rU')
  t1 = f.read()
  f.close()
  
  config = t1.split('\n')

  sessId=config[0].split('^')
  antiforgerytoken=config[1].split('^')

  return sessId, antiforgerytoken

def printResponse(methodname,req):
  print methodname
  print req.content

def invokeAPI(all_methods, method_number_to_invoke):
  method_to_invoke = method_number_map[int(method_number_to_invoke,10)]

  for m1 in all_methods:
    t1 = m1.split('^')
    if t1[0] == method_to_invoke:
      method_details = t1

  methodname = method_details[0]
  params = method_details[1]
  url = method_details[2]

  session_get_header = {'CSRF_TOKEN ': antiforgerytoken[1], 'Cookie ': 'SESSION='+sessId[1]}
  session_post_header = {'CSRF_TOKEN ': antiforgerytoken[1], 'Cookie ': 'SESSION='+sessId[1], 'Content-Type ':'application/json'}
  content_type_header = {'Content-Type ':'application/json'}

  if method_details[4] == 'Y':
    if method_details[3] == 'GET':
      req = requests.get(url, headers=session_get_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'POST':
      req = requests.post(url, headers=session_post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'PUT':
      req = requests.put(url, headers=session_post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'DELETE':
      req = requests.delete(url, headers=session_post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)

  elif method_details[4] == 'N':
    if method_details[3] == 'GET':
      req = requests.get(url, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'POST':
      req = requests.post(url, headers=content_type_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'PUT':
      req = requests.put(url, headers=content_type_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'DELETE':
      req = requests.delete(url, headers=content_type_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)

  #Print the response to the method call. Let the user make a decision, don't put intelligence in.
  printResponse(methodname,req)

def chooseAPI(all_methods):
  print "\nEnter the API number that you would like to invoke\n"
  for i in range(0,len(all_methods)):
    t1 = all_methods[i].split('^')
    print str(i)+"\t"+"|"+"\t"+t1[0]
    method_number_map[i] = t1[0]
  print '\n'

  #Accept user input
  method_number_to_invoke = raw_input('Method Number:\t')

  return method_number_to_invoke

def getAPIData():
  all_methods = []
  apiDefsFile = 'methods_authuser'

  try:
    f=open(apiDefsFile,'rU')
    t1 = f.read()
    f.close()

    all_methods = t1.split('\n')
    all_methods.pop()
  except:
    print "Unexpected error:", sys.exc_info()[0]

  return all_methods

main()
