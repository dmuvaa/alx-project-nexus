"""Utility functions for integrating with the MPesa Daraja API.

This module encapsulates calls to the MPesa API to obtain an access
token and to initiate STK push payments. In production, sensitive
credentials should be stored in a secure vault rather than
environment variables.
"""

import base64
import datetime
import os
from typing import Dict, Any

import requests


def get_access_token() -> str:
    """Obtain an OAuth access token from the MPesa API.

    The function uses the consumer key and consumer secret from the
    environment to request a bearer token. It returns the access token
    string which is valid for a limited time.

    Returns:
        A JWT access token string.
    """
    consumer_key = os.environ.get("MPESA_CONSUMER_KEY")
    consumer_secret = os.environ.get("MPESA_CONSUMER_SECRET")
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    environment = os.environ.get("MPESA_ENVIRONMENT", "sandbox")
    token_url = (
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        if environment == "sandbox"
        else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    )
    response = requests.get(token_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("access_token")


def lipa_na_mpesa(phone_number: str, amount: float, account_reference: str, transaction_desc: str) -> Dict[str, Any]:
    """Initiate an STK Push request (Lipa na MPesa online checkout).

    This function constructs the required request payload and headers,
    including encoding the password as required by the API. It returns
    the API response for further processing.

    Args:
        phone_number: The MSISDN sending the payment (format 2547XXXXXXXX).
        amount: The amount to be charged.
        account_reference: An alphanumeric reference for the transaction.
        transaction_desc: A short description of the payment.

    Returns:
        A dictionary representation of the MPesa API response.
    """
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    short_code = os.environ.get("MPESA_SHORT_CODE")
    pass_key = os.environ.get("MPESA_PASSKEY")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = f"{short_code}{pass_key}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode()
    payload = {
        "BusinessShortCode": short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": os.environ.get(
            "MPESA_CALLBACK_URL", "https://example.com/api/payments/callback/"
        ),
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }
    environment = os.environ.get("MPESA_ENVIRONMENT", "sandbox")
    request_url = (
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        if environment == "sandbox"
        else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    )
    response = requests.post(request_url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()