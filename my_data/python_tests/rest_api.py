import requests
import pprint
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import time
import sys
from os import listdir
from os.path import isfile, join
# authenticate

# A simple script to 
# 1) log in and get the session. 
# 2) upload a zip file to Data Validation servlet.

def get_session():
	#curl -k -X POST --data "action=login&username=azkaban&password=azkaban" http://localhost:8081
	url = 'http://localhost:8081'
	data = 'action=login&username=dataq&password=dataq'
	response = requests.post(url, data=data,headers={"Content-Type": "application/x-www-form-urlencoded"})
	print(response.content)
	sid=response.json()['session.id']
	return sid


def upload_json(sid,proj_name,proj_desc,proj_id,json_file_path):
	print("## in function upload_json")
	print("proj_name "+proj_name)
	print("proj_desc "+proj_desc)
	print("proj_id "+str(proj_id))
	print("json_file_path "+json_file_path)

	url = "http://localhost:8081/dvFlowUpload"
	
	headers = {'Content-type': 'application/octet-stream', 'Accept': 'application/json'}
	params = {'session.id': sid, 'project_id': proj_id,'project_description': proj_name}
	with open(json_file_path,'rb') as myfile:
	 data=myfile.read()

	response = requests.post(url, data=data, headers=headers,params=params)
	print("uploaded the job ...")
	# print(response.content)
	# print(response.request.body)
	# print(response.request.headers)
	return response.content
	
def invoke_dv_zip_upload(sid,proj_id,exec_id):
	print("##\t\tinvoke_dv_zip_upload function")
	multipart_data = MultipartEncoder(
	    fields={
	            # a file upload field
	            'file': ('sample_flow_01.zip', open('/Users/dhiraj/Desktop/sample_flow_01.zip', 'rb'),'application/zip'),
	            # plain text fields
	            'session.id': sid,
	            'jobReturnStatus': 'PASS',
	            'ajax': 'upload',
	            'execid':exec_id,
	            'job_id':'shell_echo',
	            'projectId':proj_id,
	            'resultCount':'1',
	            'expectedCount':'1'
	           }
	    )

	response = requests.post('http://localhost:8081/dvResults?action=upload', data=multipart_data,
	                  headers={'Content-Type': multipart_data.content_type})

	print(response.request.body)
	print(response.request.headers)


def create_project(sid,proj_name):
	print("##\t\tcreate_project function")
	response = requests.post('http://localhost:8081/manager?action=create', data={'session.id': sid,'name':proj_name,'description':'myp1_desc'},
	                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
	print(response.content)


def crete_wf(sid,proj_id,wf_path):
	print("##\t\tcreate_wf function")
	multipart_data = MultipartEncoder(
	    fields={
	            # a file upload field
	            'file': ('sample_flow_01.zip', open(wf_path, 'rb'),'application/zip'),
	            # plain text fields
	            'session.id': sid,
	            'ajax': 'upload',
	            'project':proj_id
	           }
	    )

	response = requests.post('http://localhost:8081/manager', data=multipart_data,
	                  headers={'Content-Type': multipart_data.content_type})

	print(response.request.body)
	print(response.request.headers)
	print(response.content)

def fetch_flows_project(sid,proj_id):
	#
	#curl -k --get --data "session.id=e0a50d95-af1c-4569-8564-65756ddfaddc&ajax=fetchprojectflows&project=a123456" https://localhost:8443/manager

	print("##\t\tfetch_flows_project function")
	response = requests.get('http://localhost:8081/manager', data={'session.id': sid,'ajax':'fetchprojectflows','project':proj_id})
	                  
	print(response.request.body)
	print(response.request.headers)
	print(response.content)
	print(response.headers)

def fetch_dv_results(sid,proj_id,flow_id):
	response = requests.get('http://localhost:8081/dvResults?action=fetch', params={'session.id': sid,'ajax':'fetch_dv_results','project_id':proj_id,'flow_id':flow_id})
	print(response.request.body)
	print(response.request.headers)
	print(response.content)
	print(response.headers)
	

def executeFlow(sid,proj_name,flow_id):
	response = requests.get('http://localhost:8081/executor', params={'session.id': sid,'ajax':'executeFlow','project':proj_name,'flow':flow_id})
	print(response.request.body)
	print(response.request.headers)
	print(response.content)
	print(response.headers)
	return response.content

def syncTest(sid):
	response = requests.get('http://localhost:8081/dvSyncServlet', params={'session.id': sid,'ajax':'executeFlow'})
	print(response.request.body)
	print(response.request.headers)
	print(response.content)
	print(response.headers)
	return response.content


def getSparkResults(sid,exec_id):
	response = requests.get('http://localhost:8081/dvFlowUpload', params={'session.id': sid,'ajax':'fetchResults','exec_id':exec_id})
	# print(response.request.body)
	# print(response.request.headers)
	# print(response.content)
	# print(response.headers)
	return response

def getAzkabanResults(sid,exec_id):
	response = requests.get('http://localhost:8081/executor', params={'session.id': sid,'ajax':'fetchexecflow','execid':exec_id})
	return response


def create_flow_test(sid,proj_name,proj_desc,proj_id,flow_json):
	ress = upload_json(sid,proj_name,proj_name,proj_id,flow_json)
	print("step 1: ")
	print(ress)
	
	ress1=json.loads(ress)

	execRes = executeFlow(sid,ress1["project_name"],ress1["flow_id"])
	execResDict = json.loads(execRes)
	print(execResDict["execid"])
	#loop 20 times: # wait for 2 min max
	print("BEGIN#####")
	for x in range(0, 10):	
		time.sleep(10)
		rress = getAzkabanResults(sid,execResDict["execid"])
		# print(rress)
		if rress.content is "":
			print("empty")
		else:
			statusRes=rress.json()
			exceptionOccurred=statusRes['status']
			if(exceptionOccurred=="SUCCEEDED"):
				print("Job completed.")	
				print("#############")
				return 0								
			elif(exceptionOccurred=="RUNNING"):
				print("The job is running..")
			else:
				print("The job status is .."+exceptionOccurred)	
				print("exiting...")
				return 1
				
		
		

def proxy_test(sid):
	response = requests.get('http://localhost:8081/proxyyy', params={'session.id': sid,'ajax':'fetchResults','targetUri':'http://localhost:9000/v1/posts'})
	print(response.request.body)
	print(response.request.headers)
	print(response.content)
	print(response.headers)

sid=get_session()
# create_flow_test(sid)
wf_path=sys.argv[1]
onlyfiles = [f for f in listdir(wf_path) if isfile(join(wf_path, f))]
index = 0
for file in onlyfiles:
	index = index + 1
	filePath=wf_path+"/"+file
	print(" "+filePath)
	projName=str(file).replace(".","")
	create_project(sid,projName)
	proj_id = index
	flow_id = 'shell_echo'

	jr=create_flow_test(sid,projName,projName,proj_id,filePath)
	print("file "+str(file)+" : "+str(jr))

print(wf_path)
# json flow -- "/Users/dhiraj/Documents/dataq/DataqAzkaban/src/main/resources/demo_1.json"
#wf_path='/Users/dhiraj/Desktop/sample_flow_01.zip'
proj_id = '1'
# exec_id = '1'
flow_id = 'shell_echo'
#create_flow_test(sid,proj_id)
# sid=get_session()
# syncTest(sid)
print(sid)


# invoke_dv_zip_upload(sid,proj_id,exec_id)

# executeFlow(sid,ress["project_id"],ress["flow_id"])
# print("sid "+sid)

# fetch_dv_results(sid,proj_id,flow_id)



# proxy_test(sid)




# executeFlow(sid,ress["project_id"],ress["flow_id"])
# print("sid "+sid)
#fetch_dv_results(sid,proj_id,flow_id)

#invoke_dv_zip_upload(sid,proj_id,exec_id)
# create_project(sid,proj_id)

#fetch_flows_project(sid,proj_id)
#fetch_flows_project('20cdcf5b-b049-499b-82ab-7d75d00f7df5','a123456789')


#
#curl -k --get --data "session.id=6c96e7d8-4df5-470d-88fe-259392c09eea&ajax=fetchprojectflows&project=a123456" https://localhost:8443/manager






#curl -k -i -H "Content-Type: multipart/mixed" -X POST --form 'session.id=ec004d76-8086-46ce-8ace-de97da0ffa20' --form 'ajax=upload' --form 'file=@/Users/dhiraj/Desktop/sample_flow_01.zip;type=application/zip' --form 'project=myp1;type/plain' https://localhost:8081/manager
