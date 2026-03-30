from datetime import date
from pydantic import BaseModel
from typing import List

from database_model import TravelPlan

class TravelPlanKeySchema(BaseModel):
    """Defines how a TravelPlan key should be represented"""
    travel_plan_key: int


class TravelPlanSchema(BaseModel):
    """Defines how a new TravelPlan should be represented"""
    # Keep types aligned with your SQL entity (INT fields).
    # If you later switch to Date in the DB, change these to `date`.
    start_date: date
    end_date: date
    travel_purpose: str
    destination: str
    origin: str
    customer_id: int


class TravelPlanViewSchema(BaseModel):
    """Defines how a TravelPlan should be returned"""
    start_date = date
    end_date = date
    travel_purpose = str
    destination = str
    origin = str
    travel_plan_key = int
    customer_id = int


class TravelPlansListSchema(BaseModel):
    """Defines how a list of TravelPlans should be returned"""
    travel_plans: List[TravelPlanViewSchema]


def show_travel_plan_view(travel_plan: TravelPlan):
    """Returns a travel plan view representation"""
    return {
        "travel_plan_key": travel_plan.travel_plan_key,
        "start_date": travel_plan.start_date.isoformat(),
        "end_date": travel_plan.end_date.isoformat(),
        "travel_purpose": travel_plan.travel_purpose,
        "destination": travel_plan.destination,
        "origin": travel_plan.origin,
        "customer_id": travel_plan.customer_id,
    }


def show_travel_plans_list(travel_plans: List[TravelPlan]):
    """Returns a list representation for travel plans"""
    return {
        "travel_plans": [show_travel_plan_view(travel_plan) for travel_plan in travel_plans]
    }
