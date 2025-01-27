import json
import boto3

s3 = boto3.client('s3')
bucket_name = 'sharedfileuploads'

def lambda_handler(event, context):
    # For Lambda Function URLs, the method is directly in requestContext
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')

    if http_method == 'GET':
        # List all objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket_name)
        result = []

        # Build a list of file information with download URLs
        for obj in objects.get('Contents', []):
            file_name = obj['Key']
            download_url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': file_name
                },
                ExpiresIn=3600
            )
            result.append({
                "fileName": file_name,
                "downloadURL": download_url
            })

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    elif http_method == 'POST':
        # Parse the request body for the file name
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('fileName', '')

        if not file_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'fileName' parameter"})
            }

        # Generate a presigned URL for uploading the file
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name
            },
            ExpiresIn=3600
        )

        return {
            'statusCode': 200,
            'body': json.dumps({"uploadURL": upload_url})
        }

    # If neither GET nor POST were called, return a 405 (Method Not Allowed)
    return {
        'statusCode': 405,
        'body': json.dumps({"error": "Method Not Allowed"})
    }