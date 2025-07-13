class TicketManagementDescription:
    # Ticket Management
    create_ticket_description = """
                    ## Create
                    To create the new ticket
                """
    update_ticket_description = """
                        ## Update
                        To update the created ticket
                    """
    view_ticket_description = """
                        ## View
                        To view the ticket based on ticket id
                    """
    list_tickets_description = """
                        ## List
                        To all the tickets in the system based on the user role
                    """
    fetch_image_description = """
                           ## Image
                           To fetch image(base 64 string) added with image name
                       """


class TicketManagementMessages:
    failed_to_add = "Failed to create ticket "
    failed_to_fetch = "Failed to fetch ticket details"
    failed_to_edit = "Failed to update ticket details"
    failed_to_list = "Failed to list ticket details"
    failed_to_fetch_image = "Failed to fetch image "
    success_add = "Successfully created the ticket"
    success_fetch = "Successfully fetched the ticket details"
    success_edit = "Successfully updated the ticket "
    success_list = "Successfully fetched the tickets"
    success_fetch_image = "Successfully fetched the image "
