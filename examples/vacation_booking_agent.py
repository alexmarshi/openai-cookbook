"""Vacation Booking Agent
=======================

This example demonstrates a minimal autonomous agent that books a vacation.
It relies on the OpenAI API for decision making and a hypothetical travel API
for flight and hotel reservations.

The script is structured as follows:
    - Parse command line arguments for origin, destination and dates
    - Interact with the OpenAI API to decide on flights and hotels
    - Call a travel API to reserve them

Both APIs expect their keys to be available as environment variables:
    OPENAI_API_KEY   - key for the OpenAI API
    TRAVEL_API_KEY   - key for the travel provider
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Any, Dict

import requests
from openai import OpenAI

data_cls = dataclass


@data_cls
class TravelPlan:
    origin: str
    destination: str
    start_date: str
    end_date: str
    flight_id: str | None = None
    hotel_id: str | None = None


class VacationAgent:
    """Autonomous agent that books flights and hotels."""

    def __init__(self, travel_key: str, openai_key: str) -> None:
        self.client = OpenAI(api_key=openai_key)
        self.travel_key = travel_key

    def _chat(self, messages: list[dict[str, str]]) -> str:
        resp = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content

    def _travel_get(self, path: str, params: Dict[str, Any]):
        base = "https://api.example-travel.com"  # hypothetical endpoint
        headers = {"Authorization": f"Bearer {self.travel_key}"}
        resp = requests.get(f"{base}/{path}", params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _travel_post(self, path: str, payload: Dict[str, Any]):
        base = "https://api.example-travel.com"  # hypothetical endpoint
        headers = {"Authorization": f"Bearer {self.travel_key}"}
        resp = requests.post(f"{base}/{path}", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def choose_flight(self, plan: TravelPlan) -> str:
        flights = self._travel_get(
            "flights/search",
            {
                "origin": plan.origin,
                "destination": plan.destination,
                "date": plan.start_date,
            },
        )
        messages = [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": f"Choose the best flight from this JSON list: {flights}"},
        ]
        selection = self._chat(messages)
        return selection.strip()

    def choose_hotel(self, plan: TravelPlan) -> str:
        hotels = self._travel_get(
            "hotels/search",
            {
                "location": plan.destination,
                "checkin": plan.start_date,
                "checkout": plan.end_date,
            },
        )
        messages = [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": f"Choose the best hotel from this JSON list: {hotels}"},
        ]
        selection = self._chat(messages)
        return selection.strip()

    def book(self, plan: TravelPlan) -> TravelPlan:
        print("Searching flights...")
        flight_id = self.choose_flight(plan)
        print(f"Selected flight {flight_id}. Booking...")
        self._travel_post("flights/book", {"flight_id": flight_id})
        plan.flight_id = flight_id

        print("Searching hotels...")
        hotel_id = self.choose_hotel(plan)
        print(f"Selected hotel {hotel_id}. Booking...")
        self._travel_post("hotels/book", {"hotel_id": hotel_id})
        plan.hotel_id = hotel_id
        return plan


def parse_args() -> TravelPlan:
    parser = argparse.ArgumentParser(description="Book a vacation via an AI agent")
    parser.add_argument("origin", help="Flight origin airport code")
    parser.add_argument("destination", help="Flight destination airport code")
    parser.add_argument("start_date", help="Travel start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="Travel end date (YYYY-MM-DD)")
    args = parser.parse_args()
    return TravelPlan(
        origin=args.origin,
        destination=args.destination,
        start_date=args.start_date,
        end_date=args.end_date,
    )


def main() -> None:
    plan = parse_args()
    travel_key = os.environ.get("TRAVEL_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not travel_key or not openai_key:
        raise RuntimeError("Both TRAVEL_API_KEY and OPENAI_API_KEY must be set")

    agent = VacationAgent(travel_key, openai_key)
    final_plan = agent.book(plan)
    summary = (
        f"Booked flight {final_plan.flight_id} and hotel {final_plan.hotel_id} "
        f"for {final_plan.origin} -> {final_plan.destination} "
        f"from {final_plan.start_date} to {final_plan.end_date}."
    )
    print(summary)


if __name__ == "__main__":
    main()
