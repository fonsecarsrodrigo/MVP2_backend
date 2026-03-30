from database_model import Customer
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List

class CustomerKeySchema(BaseModel):
    """Defines how a new Customer should be represented"""
    customer_key: int

class CustomerSchema(BaseModel):
    """Defines how a new Customer should be represented"""
    full_name: str
    date_of_birth: date
    e_mail: str
    home_cep: str
    home_street: str
    home_number: str
    home_city: str
    home_state: str
    social_number: str
    travel_plan_id: Optional[int] = None

class CustomerViewSchema(BaseModel):
    """ Define how a new Customer should be returned
    """
    full_name = str
    customer_key = int
    date_of_birth = date
    e_mail = str
    customer_since = datetime
    home_cep = str
    home_street = str
    home_number = str
    home_city = str
    home_state = str
    social_number = str
    travel_plan_id: Optional[int] = None

class CustomerSummarySchema(BaseModel):
    """Defines how a customer summary should be represented"""
    customer_key: int
    full_name: str
    date_of_birth: date


class CustomersListSchema(BaseModel):
    """Defines how a list of customer summaries should be returned"""
    customers: List[CustomerSummarySchema]

def show_customer_view(customer: Customer):
    """Returns a customer view representation
    """
    return {
        "full_name": customer.full_name,
        "customer_key": customer.customer_key,
        "date_of_birth": customer.date_of_birth.isoformat(),
        "e_mail": customer.e_mail,
        "customer_since": customer.customer_since.isoformat(),
        "home_cep": customer.home_cep,
        "home_street": customer.home_street,
        "home_number": customer.home_number,
        "home_city": customer.home_city,
        "home_state": customer.home_state,
        "social_number": customer.social_number,
        "travel_plan_id": customer.travel_plan_id,
    }


def show_customers_list(customers: List[Customer]):
    """Returns a list representation of customer summaries"""
    return {
        "customers": [
            {key: value for key, value in show_customer_view(customer).items()}
            for customer in customers
        ]
    }
