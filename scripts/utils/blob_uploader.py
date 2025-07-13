import base64
import datetime
import os

import boto3
from uuid import uuid4

from starlette.responses import FileResponse, StreamingResponse

from scripts.Common.AppConfigurations import APP_CONFIG, Services
from scripts.Common.AppConstants import ResponseMessage, Message
from scripts.utils.logger import setup_logger
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings


logger = setup_logger()

#azure

AZURE_CONNECTION_STRING = APP_CONFIG.AZURE_CONNECTION_STRING
CONTAINER_NAME = APP_CONFIG.CONTAINER_NAME

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def epoch_timestamp_generator():
    try:
        current_time = datetime.datetime.utcnow()
        current_timestamp = current_time.timestamp()
        current_time_stamp = int(current_timestamp) * 1000
        return current_time_stamp
    except Exception as e:
        logger.error("Error while epoch timestamp " + str(e))
        raise


def upload_image_to_blob(file_obj, filename: str, content_type: str) -> str:
    try:
        blob_client = container_client.get_blob_client(filename)

        blob_client.upload_blob(
            file_obj,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )

        return blob_client.url
    except Exception as e:
        logger.error(f"Exception in upload_image_to_blob {e}")
        raise

def upload_image(input_json):
    try:
        image_name = input_json.get("image_name", "") + f"_{str(epoch_timestamp_generator())}"
        image_base64 = input_json["image_data"].split(",")[1]
        image_bytes = base64.b64decode(image_base64)

        image_file_obj = BytesIO(image_bytes)
        image_url = upload_image_to_blob(
            image_file_obj,
            filename=image_name,
            content_type=input_json.get("content_type", "image/jpeg")
        )
        return image_url if input_json.get("return_file_path", False) else True

        # In Local Testing can use this for testing
        # image_name = input_json.get("image_name", "") + \
        #              f"_{str(epoch_timestamp_generator())}"
        #
        # file_base_path = os.path.join(Services.static_images)
        # if not os.path.exists(file_base_path):
        #     os.mkdir(file_base_path)
        #
        # file_path = os.path.join(file_base_path, image_name)
        #
        # with open(file_path, "wb") as f:
        #     f.write(image_bytes)
        #
        # if input_json.get("return_file_path", False):
        #     return file_path


    except Exception as e:
        logger.error(f"Exception in upload_image {e}")
        raise

def get_blob_as_stream(blob_name: str):
    try:
        blob_client = container_client.get_blob_client(blob_name)
        stream = blob_client.download_blob().readall()
        return BytesIO(stream)
    except Exception as e:
        logger.error(f"Error in get_blob_as_stream: {e}")
        return None

def fetch_image(image_name):
    """
    :param image_name: name of the image
    returns base64 encoded image data without content-type
    """
    try:
        #To Check in local
        # file_path = os.path.join(Services.static_images, image_name).replace("\\", "/")
        #
        # if not os.path.isfile(file_path):
        #     return ResponseMessage.final_json(Message.failure, message="Image does not exist")
        # return FileResponse(file_path)

        # For sending the data to UI as the base64encoded string
        # blob_client = container_client.get_blob_client(image_name)
        # blob_data = blob_client.download_blob().readall()
        # base64_data = base64.b64encode(blob_data).decode("utf-8")
        # return  base64_data

        #Sending as file response for now
        image_stream = get_blob_as_stream(image_name)
        if not image_stream:
            return ResponseMessage.final_json(Message.failure, message="Image does not exist")

        return StreamingResponse(image_stream, media_type="image/jpeg")


    except Exception as e:
        logger.error("Error in fetch image %s", str(e))
        raise