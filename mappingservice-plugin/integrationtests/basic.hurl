#Mapping service is reachable before starting with plugin
GET {{host}}
HTTP 200

GET {{host}}/api/v1/mappingAdministration/types
HTTP 200
[Captures]
mappingType: jsonpath "$[0].id"

#---------------- BEGIN Test Mapping for Thermofisher, Tescan and Jeol ----------------------------------

#Register with a very small portion of real mapping file info as dummy mapping file
POST {{host}}/api/v1/mappingAdministration/
Content-Type: multipart/form-data; boundary=boundary
[Options] #set all variables you need for further use in this hurl script
variable: id1=0
```
--boundary
Content-Disposition: form-data; name="record"; filename="blob"
Content-Type: application/json

{"mappingId":"{{id1}}","mappingType": "{{mappingType}}","title":"TF from CI test","description":"","acl":[]}
--boundary
Content-Disposition: form-data; name="document"; filename="blob"
Content-Type: application/json

{"PrivateFei.TimeOfCreation":"entry.endTime"}
--boundary--
```
HTTP 201

#Execute Mapping with Thermofisher sample
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 200
[Captures]
result1: body
[Asserts]
body contains "entry"

#Execute Mapping with image in unhandled format
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/JEOL/image000.txt;
HTTP 500

#Execute Mapping with Thermofisher sample again after failure above
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 200
[Captures]
result2: body
[Asserts]
body contains "entry"
variable "result2" == {{result1}}

#Get registered plugin etag
GET {{host}}/api/v1/mappingAdministration/{{id1}}
HTTP 200
[Captures]
etag: header "ETag"

#Delete registered plugin
DELETE {{host}}/api/v1/mappingAdministration/{{id1}}
If-Match: {{etag}}
HTTP 204


#Register with a very small portion of real mapping file info as dummy mapping file
POST {{host}}/api/v1/mappingAdministration/
Content-Type: multipart/form-data; boundary=boundary
[Options] #set all variables you need for further use in this hurl script
variable: id1=1
```
--boundary
Content-Disposition: form-data; name="record"; filename="blob"
Content-Type: application/json

{"mappingId":"{{id1}}","mappingType": "{{mappingType}}","title":"Tescan from CI test","description":"","acl":[]}
--boundary
Content-Disposition: form-data; name="document"; filename="blob"
Content-Type: application/json

{"SEM.AcceleratorVoltage":"entry.instrument.eBeamSource.accelerationVoltage.value"}
--boundary--
```
HTTP 201

#Execute Mapping with Tescan sample
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/TESCAN/tescan-minimal.hdr;
HTTP 200
[Captures]
result1: body
[Asserts]
body contains "entry"

#Execute Mapping with image in unhandled format
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM_Image-SliceImage-001.tif;
HTTP 500

#Execute Mapping with Tescan sample again after failure above
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/TESCAN/tescan-minimal.hdr;
HTTP 200
[Captures]
result2: body
[Asserts]
body contains "entry"
variable "result2" == {{result1}}

#Get registered plugin etag
GET {{host}}/api/v1/mappingAdministration/{{id1}}
HTTP 200
[Captures]
etag: header "ETag"

#Delete registered plugin
DELETE {{host}}/api/v1/mappingAdministration/{{id1}}
If-Match: {{etag}}
HTTP 204


#Register with a very small portion of real mapping file info as dummy mapping file
POST {{host}}/api/v1/mappingAdministration/
Content-Type: multipart/form-data; boundary=boundary
[Options] #set all variables you need for further use in this hurl script
variable: id1=2
```
--boundary
Content-Disposition: form-data; name="record"; filename="blob"
Content-Type: application/json

{"mappingId":"{{id1}}","mappingType": "{{mappingType}}","title":"Tescan from CI test","description":"","acl":[]}
--boundary
Content-Disposition: form-data; name="document"; filename="blob"
Content-Type: application/json

{"$CM_ACCEL_VOLT": "entry.instrument.eBeamSource.accelerationVoltage.value"}
--boundary--
```
HTTP 201

#Execute Mapping with Jeol sample
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/JEOL/image000.txt;
HTTP 200
[Captures]
result1: body
[Asserts]
body contains "entry"

#Execute Mapping with image in unhandled format
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/TESCAN/tescan-minimal.hdr;
HTTP 500

#Execute Mapping with Jeol sample again after failure above
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/images/SEM/JEOL/image000.txt;
HTTP 200
[Captures]
result2: body
[Asserts]
body contains "entry"
variable "result2" == {{result1}}

#Get registered plugin etag
GET {{host}}/api/v1/mappingAdministration/{{id1}}
HTTP 200
[Captures]
etag: header "ETag"

#Delete registered plugin
DELETE {{host}}/api/v1/mappingAdministration/{{id1}}
If-Match: {{etag}}
HTTP 204

#---------------- END Test Mapping for Thermofisher, Tescan and Jeol ----------------------------------