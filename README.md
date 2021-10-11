# AWS Rekognition API

## Description
The project is AWS Rekognition API which analyzes the photo you sent and returns the answer that is in the image.
API have 2 endpoints POST (to send image name and callback url) and GET (to get info about sent photo). And also after POST request you will get presign url to send file of photo
using PUT request finally you will get answer which contain presign url and blob id what must be used in GET request. Expiration time of presign url is 1 hour.


## Getting Started

### POST request: Example

### GET request: Example
