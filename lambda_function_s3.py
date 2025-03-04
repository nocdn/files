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
                "downloadURL": download_url,
                "fileSize": obj['Size']
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

    elif http_method == 'DELETE':
        # Parse the request body for the file name
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('fileName', '')

        if not file_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'fileName' parameter"})
            }

        # Delete the specified file from the S3 bucket
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"File '{file_name}' deleted successfully."})
        }

    elif http_method == 'PUT':
        body = json.loads(event.get('body', '{}'))
        old_file_name = body.get('oldFileName', '')
        new_file_name = body.get('newFileName', '')

        if not old_file_name or not new_file_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'oldFileName' or 'newFileName' parameter"})
            }

        # Copy the old file to the new file name
        copy_source = {
            'Bucket': bucket_name,
            'Key': old_file_name
        }

        try:
            s3.copy_object(
                Bucket=bucket_name,
                CopySource=copy_source,
                Key=new_file_name
            )
            # Delete the old file
            s3.delete_object(Bucket=bucket_name, Key=old_file_name)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"File renamed from '{old_file_name}' to '{new_file_name}' successfully."})
        }
    
    return {
        'statusCode': 405,
        'body': json.dumps({"error": "Method Not Allowed"})
    }