from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import date, datetime
from typing import Union

from database_model.base import Base

class Customer(Base):
    __tablename__ = 'customer'
    full_name = Column(String)
    customer_key = Column(Integer, primary_key=True, autoincrement=True)
    date_of_birth = Column(Date, default=date.min)
    e_mail = Column(Integer)
    customer_since = Column(DateTime)
    home_cep = Column(String)
    home_street = Column(String)
    home_number = Column(String)
    home_city = Column(String)
    home_state = Column(String)
    social_number = Column(String)
    travel_plan_id = Column(Integer, nullable=True)

    def __init__(
        self,
        full_name: str,
        date_of_birth: date,
        e_mail: int,
        home_cep: str,
        home_street: str,
        home_number: str,
        home_city: str,
        home_state: str,
        customer_since: Union[date, None] = None,
        social_number: str = "",
        travel_plan_id: Union[int, None] = None,
    ):
        """
        Creates a Customer

        Arguments:
            full_name: customer's full name
            date_of_birth: customer's date of birth
            e_mail: customer's email (as defined in the SQL schema)
            customer_since: date since when the customer has been registered
            home_cep: residential postal code (CEP)
            home_street: street name
            home_number: street number
            home_city: city (municipality)
            home_state: state (UF)
            social_number: document that uniquely identifies the customer
            travel_plan_id: optional FK to an existing travel plan
        """
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.e_mail = e_mail
        self.home_cep = home_cep
        self.home_street = home_street
        self.home_number = home_number
        self.home_city = home_city
        self.home_state = home_state
        self.social_number = social_number
        self.travel_plan_id = travel_plan_id

        # if not provided, it will default to today's date
        if customer_since:
            self.customer_since = customer_since
        else:
            self.customer_since = datetime.now()
