# E6998-Assignment-1

### 

### Developer

| Name        | UNI    |
| ----------- | ------ |
| Danling Wei | dw3033 |

### Website URL

 https://s3.amazonaws.com/e6889.com/chat.html 

### Description

​	In lambda function folder, besides L1, L2, and L0, I create a dumpDB function to use Yelp API to directly fetch data and store them in dynamoDB. Then I download result.csv from dynamoDB them transform it into sample.json which is used for OpenSearch. These two files are all in Yelp scaper script folder.

- [x] Frontend hosted on S3 - Done
- [x] API Gateway: Enable CORS - Done
- [x] Check Swagger file - Done
- [x] Lex configured 3 intents - Done
- [x] Lex errors check - Done
- [x] Yelp scraping method - Done
- [x] DynamoDB data model - Done
- [x] OpenSearch data model - Done
- [x] Cloud watch events (Eventbridge) trigger - I add trigger in LF2
- [x] SQS setup - LF1 send to queue and LF2 receive it by trigger
- [x] SNS/SES - I used SNS to send email

- **I met all the assignment requirements.**

