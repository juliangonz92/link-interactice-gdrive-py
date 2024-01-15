import os
import datetime
import subprocess
import requests
import base64
import io
import google_drive

def create_blob_from_base64(image_base64):
    try:
        # Add padding if necessary
        padded_base64 = image_base64 + '=' * (-len(image_base64) % 4)
        
        # Decode the base64 string
        image_bytes = base64.b64decode(padded_base64)
        
        # Convert the bytes to a blob
        with io.BytesIO(image_bytes) as image_bytes_io:
            blob = image_bytes_io.getvalue()
            return blob
        # image_bytes = base64.b64decode(image_base64)
        # with io.BytesIO(image_bytes) as image_bytes_io:
        #     blob = image_bytes_io.getvalue()
        #     return blob

    except Exception as e:
        raise RuntimeError("Failed to create Blob from base64 image:", str(e)) from e

def capture_image():
    # call the .sh to capture the image
    try: 
        output = subprocess.check_output(['/home/juliangonzalez/Documentos/link-interactice-gdrive-py/webcam.sh'], stderr=subprocess.STDOUT, text=True)
        lines = output.strip().split('\n')

        # Get the last line
        image_data = lines[-1]
        print(image_data)
        cleaned_string = ''.join(chr for chr in image_data if 31 < ord(chr) < 127)

        # Extract the path
        rel_path = cleaned_string.split('/')[-1]

        # Print the path
        print(rel_path)

        # # construct the full file path
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, rel_path)

        print('Image data')
        print(image_data)

        return abs_file_path, rel_path
    except Exception as e:
        raise RuntimeError(str(e)) from e

async def upload_image(image_data, name):
    try:

        # url = 'http://localhost:3000/upload'

        # # Assuming `image_data` contains the file path or binary data of the image
        # files = {'image': open(image_data, 'rb')}  # Use 'image' instead of 'file'

        # response = requests.post(url, files=files)

        # Verificar el resultado de la solicitud
        # if response.status_code == 200:
        #     print('El archivo se ha enviado exitosamente.')
        # else:
        #     print('Hubo un problema al enviar el archivo:', response.status_code)

        # headers = {'Content-Type': 'image/jpeg'}
        # files = {'image': image_data}
        # response = requests.post('http://localhost:3000/upload', headers=headers, files=files)
        # response.raise_for_status() # Raise an exception for non-200 status codes

        # data = response.json()
        data = google_drive.upload_file_drive(image_data, name)
        print('Image uploaded:', data)
        
        os.remove(image_data)
        return data

    except requests.exceptions.RequestException as error:
        print('Error uploading image:', error)
        raise

    except Exception as error:
        print('Error taking picture:', error)
        raise

async def main():
    # capture image
    image_data, rel_path = capture_image()

    # convert image to blob
    blob = create_blob_from_base64(image_data)

    # upload image
    await upload_image(image_data, rel_path)

    # print the response
    print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())