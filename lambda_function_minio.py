import json
import boto3

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url='http://vps.bartoszbak.org:9000',
        aws_access_key_id='oru5IBe9cwMxKJQNwHwd',
        aws_secret_access_key='40euNLk4zkBG9zGxEQxgBrENn2JZ5Kz0k1AZ3YFz',
        config=boto3.session.Config(signature_version='s3v4')
    )

s3 = get_minio_client()
bucket_name = 'uploads' # Changed bucket name to 'test' as requested

def lambda_handler(event, context):
    # For Lambda Function URLs, the method is directly in requestContext
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')

    if http_method == 'GET':
        # List all objects in the bucket
        try:
            objects = s3.list_objects_v2(Bucket=bucket_name)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }
        result = []

        # Build a list of file information with download URLs
        for obj in objects.get('Contents', []):
            file_name = obj['Key']
            try:
                download_url = s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': file_name
                    },
                    ExpiresIn=3600
                )
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({"error": str(e)})
                }
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
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid JSON body"})
            }
        file_name = body.get('fileName', '')

        if not file_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'fileName' parameter"})
            }

        # Generate a presigned URL for uploading the file
        try:
            upload_url = s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': file_name
                },
                ExpiresIn=3600
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({"uploadURL": upload_url})
        }

    elif http_method == 'DELETE':
        # Parse the request body for the file name
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid JSON body"})
            }
        file_name = body.get('fileName', '')

        if not file_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'fileName' parameter"})
            }

        # Delete the specified file from the S3 bucket
        try:
            s3.delete_object(Bucket=bucket_name, Key=file_name)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"File '{file_name}' deleted successfully."})
        }

    elif http_method == 'PUT':
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid JSON body"})
            }
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