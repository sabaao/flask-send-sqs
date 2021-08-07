from flask import Flask, request
import boto3

app = Flask(__name__)
app.config.from_pyfile('.env')
sqs = boto3.client('sqs')

queue_url = app.config.get('AWS_SQS_URL')

@app.route('/')
def index():
    return 'ok'

@app.route('/add', methods=['POST'])
def add():
    response = sqs.send_message(
        QueueUrl = queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )
    
    if response['MessageId']:
        return "MessageId: " + response['MessageId']
    else:
        return "Error: " + response["error_text"]
    
if(__name__=="__main__"):
    app.run()