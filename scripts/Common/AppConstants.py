class TicketStatus:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class UserRole:
    USER = "user"
    SUPPORT_TEAM = "support_team"

class Routes:
    ticket_management = "/ticket_management"

class Tags:
    ticket_management_tag = "Ticket Management"

class TicketManagement:
    create_ticket = "/create_ticket"
    update_ticket = "/update_ticket"
    view_ticket = "/view_ticket"
    list_tickets = "/list_tickets"
    fetch_image = "/fetch_image"


class General:
    application_json = 'application/json'
    un_processable_entry = 'Un processable Entity'

class Message:
    success = "success"
    failure = "failure"
    warning = "warning"


class ResponseMessage:
    @staticmethod
    def final_json(status, message, data={}, meta=None):
        if meta is None:
            json = {"status": status, "message": message, "data": data}
        else:
            json = {"status": status, "message": message, "data": data, "meta_data": meta}

        return json