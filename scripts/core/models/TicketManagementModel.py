from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional
from scripts.Common.AppConstants import General


class TicketCreate(BaseModel):
    title: str
    description: str
    comments: Optional[str] = None
    created_by: Optional[str] = None
    image_data: Optional[str] = None
    image_name: Optional[str] = None

class TicketUpdate(BaseModel):
    ticket_id: str
    comments: Optional[str] = None
    updated_by: Optional[str] = None
    status: str

class ViewTicket(BaseModel):
    ticket_id: str

class ListTickets(BaseModel):
    #can add filter and pagination if needed
    user_id: Optional[str] = None

class TicketModelResponses:
    create_ticket_responses = {
        200: {
            "description": "Success",
            "content": {
                General.application_json: {
                    "example": {

                        "status": "success",
                        "message": "Successfully created the ticket",
                        "data": {"id": "ticket_6873363d442670efffd655bd"}
                    }}}},
        401: {
            "description": "Unauthorized",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unauthorized"
                    }}}},
        422: {
            "description": General.un_processable_entry,
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unable to create the ticket"
                    }}}},
    }
    update_ticket_responses = {
        200: {
            "description": "Success",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "success",
                        "message": "Successfully updated the ticket details",
                        "data": {}
                    }}}},
        401: {
            "description": "Unauthorized",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unauthorized"
                    }}}},
        422: {
            "description": General.un_processable_entry,
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unable to update the ticket"
                    }}}},
    }
    list_ticket_responses = {
        200: {
            "description": "Success",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "success",
                        "message": "Successfully listed the tickets",
                        "data": [
                            {
                              "_id": "6873562f07cb23afbce43f2a",
                              "title": "Ticket Tittle",
                              "description": "Description of issue",
                              "comments": "Comments of Ticket",
                              "image_path": "/url",
                              "status": "open",
                              "created_by": "user_name",
                              "created_on": "2025-07-13T06:46:07Z"
                            }
                          ]
                    }}}},
        401: {
            "description": "Unauthorized",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unauthorized"
                    }}}},
        422: {
            "description": General.un_processable_entry,
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unable to list the tickets"
                    }}}},
    }

    fetch_ticket_responses = {
        200: {
            "description": "Success",
            "content": {
                General.application_json: {
                    "example": {

                        "status": "success",
                        "message": "Fetched the ticket details successfully",
                        "data": {}
                    }}}},
        401: {
            "description": "Unauthorized",
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unauthorized"
                    }}}},
        422: {
            "description": General.un_processable_entry,
            "content": {
                General.application_json: {
                    "example": {
                        "status": "failure",
                        "message": "Unable to fetch the ticket details"
                    }}}},
    }
