#Mapping service is reachable before starting with plugin
GET {{host}}
HTTP 200

#Register plugin with Thermofisher map
POST {{host}}/api/v1/mappingAdministration/
[MultipartFormData]
record: file,./mappingservice-plugin/integrationtests/ma.json;
document: file,./src/resources/maps/mapping/SEM_thermofisher.json;type=application/json
HTTP 201

#Execute Mapping with Thermofisher sample
POST {{host}}/api/v1/mappingExecution/0000
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 200
[Captures]
result1: body
[Asserts]
body contains "entry"

#Execute Mapping with image in unhandled format (change this test once the format is handled)
POST {{host}}/api/v1/mappingExecution/0000
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/JEOL/image000.txt;
HTTP 500

#Execute Mapping with Thermofisher sample again after failure above
POST {{host}}/api/v1/mappingExecution/0000
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 200
[Captures]
result2: body
[Asserts]
body contains "entry"
variable "result2" == {{result1}}

#Get registered plugin etag
GET {{host}}/api/v1/mappingAdministration/0000
HTTP 200
[Captures]
etag: header "ETag"

#Delete registered plugin
DELETE {{host}}/api/v1/mappingAdministration/0000
If-Match: {{etag}}
HTTP 204