import json
import os
import re
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag

from database_model.Customer import Customer
from database_model.TravelPlan import TravelPlan
from database_model import Session

from flask_cors import CORS

from schemas.Customer import (
    CustomerViewSchema,
    CustomerSchema,
    CustomerKeySchema,
    CustomersListSchema,
    show_customer_view,
    show_customers_list,
)
from schemas.TravelPlan import (
    TravelPlanSchema,
    TravelPlanViewSchema,
    TravelPlanKeySchema,
    TravelPlansListSchema,
    show_travel_plan_view,
    show_travel_plans_list,
)
from schemas.error import ErrorSchema, OKSchema
from sqlalchemy.exc import NoResultFound

# Create OPENAPI Info metadata for Swagger UI
info = Info(title="Bora Orneles Customer Area API", version="1.0.0")
# Create OpenAPI creates a Flask app and
# then adds OpenAPI capabilities on top of it.
app = OpenAPI(__name__, info=info)
CORS(app)

#Defines tags used to group endpoints in the API documentation.
customer_tag = Tag(name="Customer", description="Customer related database API calls")
travel_plan_tag = Tag(name="TravelPlan", description="TravelPlan related database API calls")

# Route for the home page that redirects to the OpenAPI documentation.
@app.route("/")
def home():
    return redirect("/openapi")

# ------------------------------------------------------------
# Customer Routes
# ------------------------------------------------------------
@app.post(
    "/add_customer",
    tags=[customer_tag],
    responses={"200": CustomerViewSchema, "400": ErrorSchema},
)
def add_customer(form: CustomerSchema):
    """Add a new customer to the database."""
    session = Session()
    try:
        customer = Customer(
            full_name=form.full_name,
            date_of_birth=form.date_of_birth,
            e_mail=form.e_mail,
            home_cep=form.home_cep,
            home_street=form.home_street,
            home_number=form.home_number,
            home_city=form.home_city,
            home_state=form.home_state,
            social_number=form.social_number,
            travel_plan_id=form.travel_plan_id,
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
    except Exception:
        session.rollback()
        return {"message": "Failed to Add Customer to Database"}, 400

    return show_customer_view(customer), 200

@app.get("/get_customers", tags=[customer_tag], responses={"200": CustomersListSchema, "400": ErrorSchema})
def get_customers():
    """Get all customers with their identifiers and names."""

    try:
        session = Session()
        customers = session.query(Customer).all()
    except Exception:
        return {"message": "Failed to retrieve customers from database"}, 400

    return show_customers_list(customers), 200

@app.get(
    "/get_customer",
    tags=[customer_tag],
    responses={"200": CustomerViewSchema, "400": ErrorSchema},
)
def get_customer(query: CustomerKeySchema):
    """Get a customer by ID."""

    session = Session()

    try:
        customer = (
            session.query(Customer)
            .filter(Customer.customer_key == query.customer_key)
            .first()
        )
        if customer is None:
            return {"message": "Customer not found"}, 400
    except NoResultFound:
        return {"message": "Customer not found"}, 400

    return show_customer_view(customer), 200

@app.delete(
    "/delete_customer",
    tags=[customer_tag],
    responses={"200" : OKSchema, "400": ErrorSchema},
)
def delete_customer(query: CustomerKeySchema):
    """Delete a Customer by ID."""

    session = Session()
    customer_key = query.customer_key

    customer = session.query(Customer).filter(Customer.customer_key == customer_key).first()
    if customer is None:
        return {"message": "Customer not found"}, 400

    if customer.travel_plan_id is not None:
        travel_plan = session.query(TravelPlan).filter(TravelPlan.travel_plan_key == customer.travel_plan_id).first()
        if travel_plan is not None:
            session.delete(travel_plan)
        else:
            return {"message": "Travel plan not found"}, 400

    try:
        session.delete(customer)
        session.commit()
    except Exception:
        session.rollback()
        return {"message": "Failed to delete customer from database"}, 400

    return {"message": "Customer deleted successfully"}, 200

# ------------------------------------------------------------
# Travel Plan Routes
# ------------------------------------------------------------
@app.post(
    "/add_travel_plan",
    tags=[travel_plan_tag],
    responses={"200": TravelPlanViewSchema, "400": ErrorSchema},
)
def add_travel_plan(form: TravelPlanSchema):
    """Add a new travel plan to the database."""

    session = Session()
    customer = (
        session.query(Customer)
        .filter(Customer.customer_key == form.customer_id)
        .first()
    )

    if customer is None:
        return {"message": "Customer not found"}, 400

    try:
        travel_plan = TravelPlan(
            start_date=form.start_date,
            end_date=form.end_date,
            travel_purpose=form.travel_purpose,
            destination=form.destination,
            origin=form.origin,
            customer_id=form.customer_id,
        )

        session.add(travel_plan)
        session.flush()
        session.refresh(travel_plan)

        customer.travel_plan_id = travel_plan.travel_plan_key
        session.commit()
    except Exception:
        session.rollback()
        return {"message": "Failed to Add Travel Plan to Database"}, 400

    return show_travel_plan_view(travel_plan), 200

@app.get(
    "/get_travel_plans",
    tags=[travel_plan_tag],
    responses={"200": TravelPlansListSchema, "400": ErrorSchema},
)
def get_travel_plans():
    """Get all travel plans."""

    session = Session()
    try:
        travel_plans = session.query(TravelPlan).all()
    except Exception:
        return {"message": "Failed to retrieve travel plans from database"}, 400

    return show_travel_plans_list(travel_plans), 200

@app.get(
    "/get_travel_plan",
    tags=[travel_plan_tag],
    responses={"200": TravelPlanViewSchema, "400": ErrorSchema},
)
def get_travel_plan(query: TravelPlanKeySchema):
    """Get a Travel Plan by key."""

    session = Session()
    travel_plan_key = query.travel_plan_key

    try:
        travel_plan = (
            session.query(TravelPlan)
            .filter(TravelPlan.travel_plan_key == travel_plan_key)
            .first()
        )
        if travel_plan is None:
            return {"message": "Travel plan not found"}, 400
    except NoResultFound:
        return {"message": "Travel plan not found"}, 400

    return show_travel_plan_view(travel_plan), 200

@app.delete(
    "/delete_travel_plan",
    tags=[travel_plan_tag],
    responses={"200": OKSchema, "400": ErrorSchema},
)
def delete_travel_plan(query: TravelPlanKeySchema):
    """Delete a travel plan by key."""

    session = Session()
    travel_plan_key = query.travel_plan_key

    travel_plan = session.query(TravelPlan).filter(TravelPlan.travel_plan_key == travel_plan_key).first()
    if travel_plan is None:
        return {"message": "Travel plan not found"}, 400

    customer = session.query(Customer).filter(Customer.customer_key == travel_plan.customer_id).first()
    if customer is None:
        return {"message": "Associated customer not found"}, 400

    try:
        session.delete(travel_plan)
        customer.travel_plan_id = None
        session.commit()
    except Exception:
        session.rollback()
        return {"message": "Failed to delete travel plan from database"}, 400

    return {"message": "Travel plan deleted successfully"}, 200

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
