# AWS Rekognition API

## Description
The project is AWS Rekognition API which analyzes the photo you sent and returns the answer that is in the image.
API have 2 endpoints POST (to send callback url) and GET (to get info about sent photo). And also after POST request you will get presign url to send file of photo
using PUT request finally you will get answer which contain presign_url, your callback_url and blob_id what must be used in GET request. Expiration time of presign_url is 1 hour.

## Links
POST link: https://squktjjqwa.execute-api.us-east-1.amazonaws.com/dev/blobs
GET link: https://squktjjqwa.execute-api.us-east-1.amazonaws.com/dev/blobs/{blob_id}

## Getting Started

### POST request: Example
1) For first you should to send a callback_url via POST request using POST link
<br>
![Screenshot](post_example.png)
![Screenshot](post_response_example.png)

### PUT request: Example
2) For second you should to send a photo via PUT request using presign_url got in first step.
<br>
![Screenshot](put_example.png)

### GET request: Example
3) For third you should add blob_id got in first step in the end of GET link and send GET request
<br>
![Screenshot](get_example.png)

### Finally response: Example
Finally you should check response to your callback_url
<br>
![Screenshot](webhook_response_example.png)