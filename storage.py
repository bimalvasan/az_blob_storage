import os, uuid
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def file_storage():
    local_path = './data'
    container_name = 'filecontainer' 
    local_filename = container_name + str(uuid.uuid4()) + '.txt'
    upload_file_path = os.path.join(local_path, local_filename)
    
    try:
        conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        file_write(upload_file_path)

        # Create BlobServiceClient object which will be used to create a container client 
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        
        container_client = blob_service_client.get_container_client(container_name)

        try:
            # Create the container
            container_client.create_container()
        except ResourceExistsError:
            pass
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_filename)

        print('Uploading to Azure blob storage')

        # Upload the file from local
        with open(upload_file_path, 'rb') as data:
            blob_client.upload_blob(data)

        print('Successfully uploaded the file.')

    except Exception as ex:
        print('Exception: '.format(ex))


def file_write(path):
    with open(path, 'w+') as file:
        file.write('Hello Azure blob storage. It is a sample text')

file_storage()
