from fastapi import APIRouter, UploadFile, File, Form, Query
from scripts.core.handlers.TicketManagementHandler import TicketHandler
from typing import Optional
from scripts.Common.AppConstants import Routes, Tags, TicketManagement, ResponseMessage, Message
from scripts.core.constants.TicketManagementConstants import TicketManagementDescription, TicketManagementMessages
from scripts.core.models.TicketManagementModel import TicketModelResponses, TicketCreate, TicketUpdate, ViewTicket, ListTickets
from scripts.utils.logger import setup_logger


router = APIRouter(prefix=Routes.ticket_management, tags=[Tags.ticket_management_tag])

ticket_handler_obj = TicketHandler()
logger = setup_logger()

@router.post(TicketManagement.create_ticket, description=TicketManagementDescription.create_ticket_description,
                              responses=TicketModelResponses.create_ticket_responses)
def create_ticket(req_json: TicketCreate):
    """
        Api end point for raising issues (creating tickets)
        :return:
        """
    try:
        req_json = req_json.model_dump()
        result = ticket_handler_obj.add_ticket(req_json)
        return result
    except Exception as e:
        logger.error(f"Exception while creating the ticket {e}")
        return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_add)

@router.post(TicketManagement.update_ticket, description=TicketManagementDescription.update_ticket_description,
                              responses=TicketModelResponses.update_ticket_responses)
def update_ticket(req_json: TicketUpdate):
    """
        Api end point for updating issues (creating tickets)
        :return:
        """
    try:
        req_json = req_json.model_dump()
        result = ticket_handler_obj.update_ticket(req_json)
        return result
    except Exception as e:
        logger.error(f"Exception while creating the ticket {e}")
        return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_edit)

@router.post(TicketManagement.view_ticket, description=TicketManagementDescription.view_ticket_description,
                              responses=TicketModelResponses.fetch_ticket_responses)
def get_ticket(req_json: ViewTicket):
    """
        Api end point for fetch ticket details
        :return:
        """
    try:
        req_json = req_json.model_dump()
        result = ticket_handler_obj.view_ticket(req_json)
        return result
    except Exception as e:
        logger.error(f"Exception while fetching the ticket {e}")
        return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_fetch)


@router.post(TicketManagement.list_tickets, description=TicketManagementDescription.list_tickets_description,
                              responses=TicketModelResponses.list_ticket_responses)
def list_tickets(req_json: Optional[ListTickets] = None):
    """
        Api end point to list all tickets
        :return:
        """
    try:
        req_json = req_json.model_dump() if req_json else None
        result = ticket_handler_obj.list_tickets(req_json)
        return result
    except Exception as e:
        logger.error(f"Exception while listing the tickets {e}")
        return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_list)


@router.post(TicketManagement.fetch_image, description=TicketManagementDescription.fetch_image_description,
                              )
def fetch_image_data(image_name: str):
    """
        This method to fetch encode base64 image string
        :param image_name:
    """
    try:
        resp = ticket_handler_obj.fetch_images(image_name)
        return resp
    except Exception as e:
        logger.error(f"Exception in fetch image  {e}")
        return ResponseMessage.final_json(Message.failure, TicketManagementMessages.failed_to_fetch_image)

