'''
This is a simple client to invoke any of the REST API methods which need BASIC authentication. Make sure you enter valid usernames and passwords in the creds hash on line 10 in this program before continuing :) 

If you do not want to study traffic that is sent by the client, edit the code to communicate directly with the server by removing the "proxies" part from the invokeAPI method. If you DO pass traffic through Burp, ensure that you have the SUN JDK configured and not OpenJDK :)

Here is how you invoke it:

python invoke_api_with_basicauth.py
'''

import sys
import base64
import requests

#Here is a list of credentials that you use to invoke every single method. Tweak this list as you choose :). You could enter incorrect creds
#to check who does NOT have access too. Play around.
creds = {'valid_user':'valid_password'}

method_number_map = {}

def print_response(methodname,req):
  print methodname
  print req.content

def invoke_api(all_methods, method_number_to_invoke):
  method_to_invoke = method_number_map[int(method_number_to_invoke,10)]

  for m1 in all_methods:
    t1 = m1.split('^')
    if t1[0] == method_to_invoke:
      method_details = t1

  methodname = method_details[0]
  params = method_details[1]
  url = method_details[2]

  for username,password in creds.iteritems():
    get_header = {'Authorization ':'Basic '+base64.b64encode(username+':'+password)}
    post_header = {'Authorization ':'Basic '+base64.b64encode(username+':'+password), 'Content-Type ':'application/json'}

    if method_details[3] == 'GET' and method_details[4] == 'N':
      req = requests.get(url, headers=get_header, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'POST' and method_details[4] == 'N':
      req = requests.post(url, headers=post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'PUT' and method_details[4] == 'N':
      req = requests.put(url, headers=post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)
    elif method_details[3] == 'DELETE' and method_details[4] == 'N':
      req = requests.delete(url, headers=post_header, data=params, proxies={"https": "https://127.0.0.1:8080"}, verify=False)

    #Print the response to the method call. Let the user make a decision, don't put intelligence in.
    print_response(methodname,req)

def choose_api(all_methods):
  print "\nEnter the API number that you would like to invoke\n"
  for i in range(0,len(all_methods)):
    t1 = all_methods[i].split('^')
    print str(i)+"\t"+"|"+"\t"+t1[0]
    method_number_map[i] = t1[0]
  print '\n'

  #Accept user input
  method_number_to_invoke = raw_input('Method Number:\t')

  return method_number_to_invoke

def get_api_data():
  all_methods = []
  apidefsfile = 'methods_basic'

  try:
    with open(apidefsfile,'rU') as f:
      t1 = f.read()

    all_methods = t1.split('\n')
    all_methods.pop()
  except:
    sys.stderr.write("Unexpected error:", sys.exc_info()[0])

  return all_methods

if __name__ == "__main__":
  #Get all the APIs and the parameters that need to be sent with it
  all_methods = get_api_data()

  #Menu driven option which lets the user choose which API to invoke
  method_number_to_invoke = choose_api(all_methods)

  #Actually invoke the API
  invoke_api(all_methods, method_number_to_invoke)
