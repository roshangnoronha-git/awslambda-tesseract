
import json
import urllib.parse
import boto3
#from google.cloud import vision
import cv2
import pytesseract
import numpy as np
s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
    
        bucket = "Inser_bucket_name"
        # fetching object from bucket
        file_obj = s3.get_object(Bucket=bucket, Key=key)
        # reading the file content in bytes
        file_content = file_obj["Body"].read()

        # creating 1D array from bytes data range between[0,255]
        np_array = np.fromstring(file_content, np.uint8)
        # decoding array
        image_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # converting image from RGB to Grayscale
        image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        
        
        image=image[int(0.9*image.shape[0]):]
        image=cv2.threshold(image,122,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU,)[1]
        data=pytesseract.image_to_string(image)
        data= ' '.join(data.split('\n'))
        data=data.lower()
        if '1500' in data or 'cms-1500' in data :
            form_type = 0
            print('Type : 1500')
            return 
            {
            'message':'Input form is of type HCFA (CMS 1500)'
            }
        elif '1450' in data or 'cms-1450' in data or 'ub-04' in data:
            form_type = 1
            print('Type: 1450')
            return 
            {
            'message':'Input form is of type UB-04 (CMS 1450)'
            }
        elif 'j430d' in data or 'ada' in data or 'j430' in data or  'j431' in data or 'j423' in data or 'j433' in data or 'j434' in data:
            form_type=3
            print('Type: ADA')
            return 
            {
            'message':'Input form is of type ADA'
            }
        else:
            print('Unidentified')
            return 
            {
            'message':'Input form is unidentifiable'
            }

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


