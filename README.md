Find the hosted endpoint below:




# 🧠 Bitespeed Backend Task: Identity Reconciliation

This repository contains the solution to the Bitespeed Backend Task for reconciling customer identities across multiple purchases on FluxKart.

---

## 🔗 Hosted API

📍 Live Endpoint: https://bitespeed-identity-yo91.onrender.com/docs 


---

## 📦 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLite (can be swapped with PostgreSQL)
- **Deployment**: Render.com
- **ORM**: SQLAlchemy

---

## 📌 Problem Statement

Bitespeed needs to uniquely identify and track customers who may use different emails or phone numbers across multiple purchases. This system:

- Identifies whether a contact already exists
- Links new contact info with existing data
- Maintains one `primary` contact and all other linked as `secondary`

---

## 🛠️ API Endpoint

### `POST /identify`

**Request Body** (JSON):
```json
{
  "email": "string",
  "phoneNumber": 0
}
