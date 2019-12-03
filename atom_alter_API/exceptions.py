#
# Atomars API exceptions
#

class BaseAtomarsAPIError(Exception):
    '''
    Base error for Atomars API
    '''
    pass

class HTTPRequestError(BaseAtomarsAPIError):
    '''
    Base error for any exceptions caused by communication with remote server
    '''
    pass

class BadRequestError(HTTPRequestError):
    '''
    Error 400 from atomars
    '''
    pass

class UnauthorizedError(HTTPRequestError):
    '''
    Error 401 from atomars
    '''
    pass

class APIResponseError(Exception):
    '''
    Base exception for errors with the response from the API
    '''
    pass

class APIOperationStatusError(APIResponseError):
    '''
    The API returned a response with http status 200, but the json encoded status was not true
    '''
    pass



class HeaderCreationError(BaseAtomarsAPIError):
    '''
    Raised when there is an error when creating the headers or signature
    '''
    pass

class LoginError(BaseAtomarsAPIError):
    '''
    Raised when there is an error logging in
    '''
    pass

class APIExecutionError(BaseAtomarsAPIError):
    '''
    Raised when the API was not able to perform the request
    '''
    pass

