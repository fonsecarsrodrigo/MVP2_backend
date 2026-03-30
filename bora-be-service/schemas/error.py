from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define how an error is represented
    """
    message: str


class OKSchema(BaseModel):
    """ Define how an ok is represented
    """
    message: str