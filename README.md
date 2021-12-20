# [Skill NER with Argon Dashboard Flask Template and AWS]
The goal of this project is to deploy a web app that can do NER based on my [previous spaCy project](https://github.com/ChienYao-Lin/JobSkillSet.git). This app will be deployed on AWS Elastic Beanstalk with a Docker container.  At the same time, the NER model will be deployed on AWS Lambda and the spaCy package will be installed on the lambda layer. 

![](https://github.com/ChienYao-Lin/Flask-App-With-NER-Model-On-AWS/blob/main/images/demo.png)
![](https://github.com/ChienYao-Lin/Flask-App-With-NER-Model-On-AWS/blob/main/images/AWS_Diagram.jpeg)
<br />

## Requirements

- AWS CLI
```bash
$ pip install awscli
```

- AWS EB CLI ([Installation Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html))
```bash
$ # Quick Install (MacOS)
$ brew install awsebcli
```

<br />

## Deployment

> UNZIP the sources or clone the private repository. After getting the code

```bash
$ # Get the code
$ git clone git url
$ cd wordir
```

> Deploy the Docker container on [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elastic-beanstalk/index.html)

```bash
$ # Initial the app
$ eb init -p docker application-name -r region
$ 
$ # Deploy the app
$ eb create environment-name

```

> Build the DynamoDB for storing user data
```bash
$ aws dynamodb create-table \
   --table-name Users \
   --attribute-definitions \
       AttributeName=username,AttributeType=S \
   --key-schema AttributeName=username,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
   --table-class STANDARD
```

* **NOTE**: Remember the **region** which table **Users** is located, we will use it to set the environment variables of the web app. You can find the region name by use the command.
```bash
$ aws configure get region
```

> Create the Lambda function and the API Gateway
#### Create the Lambda function
1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.
2. Choose **Create function**.
3. Under **Basic information**, do the following:
    1. For Function name, enter **skill-ner**. 
    2. For Runtime, confirm that **Python 3.8** is selected.
4. Choose **Create** function.
5. Choose **Upload from** function and then choose **.zip file**.
6. Choose **lambda.zip** to deploy.

#### Create Layer
Because the size of **layer.zip** is greater than 50 MB, we have to upload the file to S3.
1. Open the [Layers page](https://console.aws.amazon.com/lambda/home#/layers) of the Lambda console.
2. Choose **Create layer**.
3. For Layer name, enter **spaCy**.
4. Choose **Upload a file from Amazon S3**. Then, for **Amazon S3 link URL**, enter the URL link we just upload to S3.
5. For **Compatible runtimes**, choose **Python 3.8**.
6. Choose Create.

#### Link the Layer to Lambda function
1. Choose **Add a layer** in the **skill-ner** page.
2. Choose **Custom Layers** and then choose the layer we just create.
3. Choose **Add**

#### Add API Gateway Trigger
1. Choose **Add Trigger** in the **skill-ner** page.
2. Choose **API Gateway** as the trigger.
3. Choose **Create an API**.
4. Choose **REST API**.
5. Choose **API key** as the security mechanism.
6. Choose **Add**

Note down the **API endpoint URL** and the **API key**.

> Set up the Elastic Beanstalks environments
For the access key and secret key, you can just your root account key. For security concerns, you also can create an IAM user with only **AmazonDynamoDBFullAccess** policy and use its access key and secret key.


```bash
$ eb setenv AWS_ACCESS_KEY_ID=AWS_KEY \
                  AWS_SECRET_ACCESS_KEY=SECRET_KEY \
                  SKILL_API_KEY=API_KEY \
                  SKILL_ENDPOINT=API_ENDPOINT_URL \
                  TABLE_REGION=USERS_REGION
```

> Open the web app
```bash
$ eb open
```

<br />

## Reference
Amazon Web Services 2021, AWS Elastic Beanstalk Developer Guide - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg
Creative Tim and AppSeed 2021, Argon Dashboard Flask - https://github.com/creativetimofficial/argon-dashboard-flask.git
Matthew Mascioni 2020, Using external Python packages with AWS Lambda layers - https://dev.to/mmascioni/using-external-python-packages-with-aws-lambda-layers-526o
Flask, User’s Guide - https://flask.palletsprojects.com/en/2.0.x/





