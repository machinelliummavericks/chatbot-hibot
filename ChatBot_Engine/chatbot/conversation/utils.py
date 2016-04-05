import time

def get_response_statements(statement_list):
    """
    Filter out all statements that are not in response to another statement.
    A statement must exist which lists the closest matching statement in the
    in_response_to field. Otherwise, the logic adapter may find a closest
    matching statement that does not have a known response.
    """

    responses = set()
    to_remove = list()
    to_keep = list()

    for statement in statement_list:
        for response in statement.in_response_to:
            responses.add(response.text)

    for statement in statement_list:
        if statement.text not in responses:
            to_remove.append(statement)

    '''
    THIS CALL TAKES THE MOST TIME IN THE CODE TO EXECUTE
    REPLACING WITH SOMETHING FASTER. INSTEAD OF USING A REMOVE
    CALL JUST USE 'if statement.text in responses:'
    '''
    #for statement in to_remove:
    #    statement_list.remove(statement)
    for statement in statement_list:
        if statement.text in responses:
            to_keep.append(statement)
    statement_list =  to_keep

    #print set(statement_list) == set(to_keep)

    return statement_list
