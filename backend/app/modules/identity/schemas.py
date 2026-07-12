"""Identity module Pydantic schemas — API in/out shapes.

Kept separate from SQLAlchemy models per DOC-130 §3 module anatomy
(schemas.py distinct from models.py). These are the shapes CI generates the
TypeScript SDK from.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


Role = Literal["viewer", "member", "manager", "admin", "owner"]


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")


class OrganizationOut(BaseModel):
    id: str
    name: str
    slug: str
    workos_org_id: str | None
    created_at: datetime


class MemberOut(BaseModel):
    id: str
    org_id: str
    subject_id: str
    email: EmailStr
    role: Role
    status: Literal["pending", "active", "suspended", "removed"]
    created_at: datetime


class InviteCreate(BaseModel):
    email: EmailStr
    role: Literal["viewer", "member", "manager", "admin"] = "member"


class InviteOut(BaseModel):
    id: str
    org_id: str
    email: EmailStr
    role: Literal["viewer", "member", "manager", "admin"]
    status: Literal["pending", "accepted", "revoked", "expired"]
    token: str
    expires_at: datetime


class InviteAccept(BaseModel):
    token: str
    subject_id: str = Field(min_length=1, max_length=128)


class RoleChange(BaseModel):
    role: Role
