import datetime

from scripts.core.persistence.TicketManagementPersistence import (
    insert_ticket,
    modify_ticket,
    fetch_ticket,
    fetch_tickets_by_user
)
from scripts.utils.blob_uploader import upload_image, fetch_image
from scripts.Common.AppConstants import TicketStatus, ResponseMessage, Message
from scripts.core.constants.TicketManagementConstants  import TicketManagementMessages
from scripts.utils.logger import setup_logger

logger = setup_logger()

class TicketHandler:

    def timestamp_generator(self):
        try:
            return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.error("Error while generating timestamp %s", str(e))
            raise

    def add_ticket(self, input_json):
        try:
            image_path = None
            if input_json.get("image_name", None):
                image_json = {
                              "image_name": input_json.get("image_name"),
                              "image_data": input_json.get("image_data"),
                              "return_file_path": True
                              }
                image_path = upload_image(image_json)
            current_time = self.timestamp_generator()
            # For now placing the user as static user if not provided from payload, get user from request header or using tokens dynamically
            created_by = input_json.get("created_by") if input_json and input_json.get("created_by", None) else 'static_user'
            ticket_data = {
                "title": input_json.get("title", None),
                "description": input_json.get("description", None),
                "comments": input_json.get("comments", None),
                "image_path": image_path,
                "status": TicketStatus.OPEN,
                "created_by": created_by,
                "created_on": current_time
            }
            ticket_id = insert_ticket(ticket_data)
            logger.info(f"Ticket created by '{created_by}': {ticket_id}")
            return ResponseMessage.final_json(Message.success, TicketManagementMessages.success_add, data={ "ticket_id": ticket_id})
        except Exception as e:
            logger.error(f"Exception in  add_ticket {e}")
            return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_add)

    def update_ticket(self, input_json):
        try:
            success = modify_ticket(input_json)
            logger.info(f"""Ticket {input_json.get("ticket_id")} updated  by {input_json.get("updated_by")}""")
            if success:
                return ResponseMessage.final_json(Message.success, TicketManagementMessages.success_edit)
            else:
                return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_edit)
        except Exception as e:
            logger.error(f"Exception in  update_ticket {e}")
            return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_edit)



    def view_ticket(self, req_json):
        try:
            data = fetch_ticket(req_json.get("ticket_id"))
            return ResponseMessage.final_json(Message.success, TicketManagementMessages.success_fetch, data = data)
        except Exception as e:
            logger.error(f"Exception in  view_ticket {e}")
            return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_fetch)

    def list_tickets(self, input_json):
        try:
            all_tickets = fetch_tickets_by_user(input_json)
            return ResponseMessage.final_json(Message.success, TicketManagementMessages.success_fetch, data = all_tickets)
        except Exception as e:
            logger.error(f"Exception in  list_tickets {e}")
            return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_list)

    def fetch_images(self, input_json):
        try:
            return fetch_image(input_json)
        except Exception as e:
            logger.error(f"Exception in  fetch_images {e}")
            return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_fetch_image)
