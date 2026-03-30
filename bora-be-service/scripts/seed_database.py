"""Seed travel plans and customers via the running HTTP API (add_customer / add_travel_plan).

POST bodies use application/x-www-form-urlencoded to match flask_openapi3 `form:` validation.
"""

from __future__ import annotations

import json
import os
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Default matches `make run` / `flask run --port=5001`
DEFAULT_API_BASE = "http://0.0.0.0:5001"


TRAVEL_PLANS = [
    {
        "start_date": date(2025, 2, 26),
        "end_date": date(2025, 3, 5),
        "travel_purpose": "Carnaval vacation",
        "destination": "Rio de Janeiro",
        "origin": "Sao Paulo",
        "target_customer_index": 1,
    },
    {
        "start_date": date(2025, 1, 15),
        "end_date": date(2025, 1, 25),
        "travel_purpose": "Beach retreat",
        "destination": "Florianopolis",
        "origin": "Curitiba",
        "target_customer_index": 3,
    },
    {
        "start_date": date(2025, 7, 10),
        "end_date": date(2025, 7, 18),
        "travel_purpose": "Festival visit",
        "destination": "Salvador",
        "origin": "Recife",
        "target_customer_index": 5,
    },
    {
        "start_date": date(2025, 5, 5),
        "end_date": date(2025, 5, 15),
        "travel_purpose": "Eco tour",
        "destination": "Manaus",
        "origin": "Belem",
        "target_customer_index": 7,
    },
    {
        "start_date": date(2025, 9, 2),
        "end_date": date(2025, 9, 6),
        "travel_purpose": "Business meetings",
        "destination": "Porto Alegre",
        "origin": "Brasilia",
        "target_customer_index": 9,
    },
]


CUSTOMERS_DATA = [
    {
        "full_name": "Ana Beatriz Souza",
        "date_of_birth": date(1990, 5, 14),
        "e_mail": "ana.souza@example.com",
        "home_cep": "01310-100",
        "home_street": "Rua das Mangueiras",
        "home_number": "123",
        "home_city": "Sao Paulo",
        "home_state": "SP",
        "social_number": "SN-0001",
        "travel_plan_id": None,
    },
    {
        "full_name": "Bruno Machado",
        "date_of_birth": date(1985, 8, 22),
        "e_mail": "bruno.machado@example.com",
        "home_cep": "01310-101",
        "home_street": "Avenida Brasil",
        "home_number": "456",
        "home_city": "Rio de Janeiro",
        "home_state": "RJ",
        "social_number": "SN-0002",
        "travel_plan_id": None,
    },
    {
        "full_name": "Carla Menezes",
        "date_of_birth": date(1992, 1, 5),
        "e_mail": "carla.menezes@example.com",
        "home_cep": "01310-102",
        "home_street": "Rua Ipe Roxo",
        "home_number": "789",
        "home_city": "Curitiba",
        "home_state": "PR",
        "social_number": "SN-0003",
        "travel_plan_id": None,
    },
    {
        "full_name": "Daniel Oliveira",
        "date_of_birth": date(1988, 3, 19),
        "e_mail": "daniel.oliveira@example.com",
        "home_cep": "01310-103",
        "home_street": "Rua das Palmeiras",
        "home_number": "321",
        "home_city": "Belo Horizonte",
        "home_state": "MG",
        "social_number": "SN-0004",
        "travel_plan_id": None,
    },
    {
        "full_name": "Eduarda Campos",
        "date_of_birth": date(1995, 11, 30),
        "e_mail": "eduarda.campos@example.com",
        "home_cep": "01310-104",
        "home_street": "Rua das Flores",
        "home_number": "654",
        "home_city": "Porto Alegre",
        "home_state": "RS",
        "social_number": "SN-0005",
        "travel_plan_id": None,
    },
    {
        "full_name": "Felipe Araujo",
        "date_of_birth": date(1991, 4, 2),
        "e_mail": "felipe.araujo@example.com",
        "home_cep": "01310-105",
        "home_street": "Rua do Sol",
        "home_number": "987",
        "home_city": "Salvador",
        "home_state": "BA",
        "social_number": "SN-0006",
        "travel_plan_id": None,
    },
    {
        "full_name": "Gabriela Lima",
        "date_of_birth": date(1983, 7, 17),
        "e_mail": "gabriela.lima@example.com",
        "home_cep": "01310-106",
        "home_street": "Rua da Paz",
        "home_number": "258",
        "home_city": "Recife",
        "home_state": "PE",
        "social_number": "SN-0007",
        "travel_plan_id": None,
    },
    {
        "full_name": "Henrique Borges",
        "date_of_birth": date(1994, 9, 9),
        "e_mail": "henrique.borges@example.com",
        "home_cep": "01310-107",
        "home_street": "Rua das Laranjeiras",
        "home_number": "369",
        "home_city": "Brasilia",
        "home_state": "DF",
        "social_number": "SN-0008",
        "travel_plan_id": None,
    },
    {
        "full_name": "Isabela Nunes",
        "date_of_birth": date(1987, 2, 27),
        "e_mail": "isabela.nunes@example.com",
        "home_cep": "01310-108",
        "home_street": "Avenida Atlantica",
        "home_number": "147",
        "home_city": "Fortaleza",
        "home_state": "CE",
        "social_number": "SN-0009",
        "travel_plan_id": None,
    },
    {
        "full_name": "Joao Pedro Carvalho",
        "date_of_birth": date(1993, 12, 12),
        "e_mail": "joao.carvalho@example.com",
        "home_cep": "01310-109",
        "home_street": "Rua Santa Clara",
        "home_number": "753",
        "home_city": "Manaus",
        "home_state": "AM",
        "social_number": "SN-0010",
        "travel_plan_id": None,
    },
]


def _form_body(payload: dict) -> bytes:
    """Build x-www-form-urlencoded body; matches flask_openapi3 `form:` parsing (not JSON)."""
    pairs: list[tuple[str, str]] = []
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, date):
            pairs.append((key, value.isoformat()))
        else:
            pairs.append((key, str(value)))
    return urlencode(pairs).encode("utf-8")


def _post_form(base_url: str, path: str, payload: dict) -> dict:
    url = f"{base_url.rstrip('/')}{path}"
    body = _form_body(payload)
    req = Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        try:
            detail = json.loads(err_body) if err_body else {}
        except json.JSONDecodeError:
            detail = {"message": err_body}
        msg = detail.get("message", detail) if isinstance(detail, dict) else detail
        raise RuntimeError(f"{path} failed (HTTP {e.code}): {msg}") from e
    except URLError as e:
        raise RuntimeError(
            f"Could not reach API at {base_url}. Start the server (e.g. `make run`). "
            f"Underlying error: {e}"
        ) from e


def seed_database(api_base: str | None = None) -> None:
    """POST customers then travel plans; `/add_travel_plan` links each plan to its customer."""
    base = (api_base or os.environ.get("SEED_API_BASE", DEFAULT_API_BASE)).rstrip("/")

    customers_by_index: dict[int, int] = {}
    for idx, data in enumerate(CUSTOMERS_DATA, start=1):
        out = _post_form(base, "/add_customer", dict(data))
        customers_by_index[idx] = int(out["customer_key"])

    for plan in TRAVEL_PLANS:
        target = plan["target_customer_index"]
        customer_id = customers_by_index.get(target)
        if customer_id is None:
            raise ValueError(f"No customer for travel plan target index {target}")
        _post_form(
            base,
            "/add_travel_plan",
            {
                "start_date": plan["start_date"],
                "end_date": plan["end_date"],
                "travel_purpose": plan["travel_purpose"],
                "destination": plan["destination"],
                "origin": plan["origin"],
                "customer_id": customer_id,
            },
        )

    print(
        f"Inserted {len(TRAVEL_PLANS)} travel plans and {len(CUSTOMERS_DATA)} customers via {base}."
    )


if __name__ == "__main__":
    seed_database()
