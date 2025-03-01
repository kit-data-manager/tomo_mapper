GET {{host}}
HTTP 200

POST {{host}}/api/v1/mappingAdministration/
[MultipartFormData]
record: file,./mappingservice-plugin/integrationtests/ma.json;
document: file,./src/resources/maps/mapping/SEM_thermofisher.json;type=application/json
HTTP 201

POST {{host}}/api/v1/mappingExecution/0000
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 200