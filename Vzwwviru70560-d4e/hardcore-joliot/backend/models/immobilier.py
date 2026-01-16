"""
CHE·NU™ V75 - Immobilier Models
Complete real estate management system.

Quebec TAL compliance included.

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, Text, JSON, Numeric
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.dataspace import DataSpace
    from models.identity import Identity


class PropertyType(str, Enum):
    """Property types."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    LAND = "land"
    MIXED = "mixed"


class OwnershipType(str, Enum):
    """Ownership types."""
    PERSONAL = "personal"
    ENTERPRISE = "enterprise"
    INVESTMENT = "investment"


class PropertyStatus(str, Enum):
    """Property status."""
    ACTIVE = "active"
    FOR_SALE = "for_sale"
    SOLD = "sold"
    ARCHIVED = "archived"


class UnitType(str, Enum):
    """Unit types."""
    APARTMENT = "apartment"
    COMMERCIAL = "commercial"
    STORAGE = "storage"
    PARKING = "parking"


class UnitStatus(str, Enum):
    """Unit status."""
    VACANT = "vacant"
    OCCUPIED = "occupied"
    RENOVATING = "renovating"
    UNAVAILABLE = "unavailable"


class TenantStatus(str, Enum):
    """Tenant status."""
    ACTIVE = "active"
    NOTICE_GIVEN = "notice_given"
    ENDED = "ended"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    RECEIVED = "received"
    LATE = "late"
    PARTIAL = "partial"
    BOUNCED = "bounced"


class PaymentMethod(str, Enum):
    """Payment methods."""
    CHEQUE = "cheque"
    TRANSFER = "transfer"
    CASH = "cash"
    INTERAC = "interac"


class MaintenanceCategory(str, Enum):
    """Maintenance categories."""
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    HVAC = "hvac"
    APPLIANCE = "appliance"
    STRUCTURAL = "structural"
    OTHER = "other"


class MaintenancePriority(str, Enum):
    """Maintenance priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class MaintenanceStatus(str, Enum):
    """Maintenance status."""
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Property(Base):
    """
    Property model.
    
    Represents a real estate property with all details
    including Quebec-specific compliance fields.
    """
    
    __tablename__ = "properties"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    dataspace_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="CASCADE"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    property_type = Column(String(50), nullable=False)
    ownership_type = Column(String(50), nullable=False)
    
    # Address
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    province = Column(String(50), default="QC")
    postal_code = Column(String(10))
    country = Column(String(50), default="Canada")
    
    # Coordinates (for mapping)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    
    # Property Details
    lot_size_sqft = Column(Numeric(12, 2))
    building_size_sqft = Column(Numeric(12, 2))
    year_built = Column(Integer)
    num_units = Column(Integer, default=1)
    num_bedrooms = Column(Integer)
    num_bathrooms = Column(Numeric(3, 1))
    
    # Financial
    purchase_price = Column(Numeric(12, 2))
    purchase_date = Column(Date)
    current_value = Column(Numeric(12, 2))
    last_valuation_date = Column(Date)
    
    # Status
    status = Column(String(20), default=PropertyStatus.ACTIVE.value)
    
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    units = relationship("PropertyUnit", back_populates="property", cascade="all, delete-orphan")
    tenants = relationship("Tenant", back_populates="property", cascade="all, delete-orphan")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="property", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Property {self.address_line1}, {self.city}>"
    
    @property
    def full_address(self) -> str:
        """Get full formatted address."""
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.append(f"{self.city}, {self.province} {self.postal_code}")
        return ", ".join(parts)
    
    @property
    def total_monthly_rent(self) -> Decimal:
        """Calculate total monthly rent from all units."""
        if self.units:
            return sum(u.monthly_rent or Decimal(0) for u in self.units)
        return Decimal(0)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy rate."""
        if not self.units:
            return 0.0
        occupied = sum(1 for u in self.units if u.status == UnitStatus.OCCUPIED.value)
        return (occupied / len(self.units)) * 100
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "dataspace_id": str(self.dataspace_id),
            "property_type": self.property_type,
            "ownership_type": self.ownership_type,
            "address": {
                "line1": self.address_line1,
                "line2": self.address_line2,
                "city": self.city,
                "province": self.province,
                "postal_code": self.postal_code,
                "country": self.country,
                "full": self.full_address,
            },
            "coordinates": {
                "latitude": float(self.latitude) if self.latitude else None,
                "longitude": float(self.longitude) if self.longitude else None,
            },
            "details": {
                "lot_size_sqft": float(self.lot_size_sqft) if self.lot_size_sqft else None,
                "building_size_sqft": float(self.building_size_sqft) if self.building_size_sqft else None,
                "year_built": self.year_built,
                "num_units": self.num_units,
                "num_bedrooms": self.num_bedrooms,
                "num_bathrooms": float(self.num_bathrooms) if self.num_bathrooms else None,
            },
            "financial": {
                "purchase_price": float(self.purchase_price) if self.purchase_price else None,
                "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
                "current_value": float(self.current_value) if self.current_value else None,
                "total_monthly_rent": float(self.total_monthly_rent),
            },
            "status": self.status,
            "occupancy_rate": self.occupancy_rate,
            "units_count": len(self.units) if self.units else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PropertyUnit(Base):
    """Individual unit within a property."""
    
    __tablename__ = "property_units"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    
    unit_number = Column(String(20))
    unit_type = Column(String(50))
    
    size_sqft = Column(Numeric(10, 2))
    num_bedrooms = Column(Integer)
    num_bathrooms = Column(Numeric(3, 1))
    
    monthly_rent = Column(Numeric(10, 2))
    
    status = Column(String(20), default=UnitStatus.VACANT.value)
    
    metadata = Column(JSON, default=dict)
    
    # Relationships
    property = relationship("Property", back_populates="units")
    tenants = relationship("Tenant", back_populates="unit")
    
    def __repr__(self):
        return f"<PropertyUnit {self.unit_number}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "property_id": str(self.property_id),
            "unit_number": self.unit_number,
            "unit_type": self.unit_type,
            "size_sqft": float(self.size_sqft) if self.size_sqft else None,
            "num_bedrooms": self.num_bedrooms,
            "num_bathrooms": float(self.num_bathrooms) if self.num_bathrooms else None,
            "monthly_rent": float(self.monthly_rent) if self.monthly_rent else None,
            "status": self.status,
        }


class Tenant(Base):
    """
    Tenant model with Quebec TAL compliance.
    """
    
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("property_units.id"))
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    # Personal info (Enterprise identity only - GOUVERNANCE)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    
    # Lease info
    lease_start = Column(Date, nullable=False)
    lease_end = Column(Date)
    monthly_rent = Column(Numeric(10, 2), nullable=False)
    security_deposit = Column(Numeric(10, 2))
    
    status = Column(String(20), default=TenantStatus.ACTIVE.value)
    
    # Quebec TAL compliance
    tal_registered = Column(Boolean, default=False)
    tal_registration_number = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="tenants")
    unit = relationship("PropertyUnit", back_populates="tenants")
    payments = relationship("RentPayment", back_populates="tenant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tenant {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    @property
    def is_lease_active(self) -> bool:
        """Check if lease is currently active."""
        today = date.today()
        if self.lease_end:
            return self.lease_start <= today <= self.lease_end
        return self.lease_start <= today
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "property_id": str(self.property_id),
            "unit_id": str(self.unit_id) if self.unit_id else None,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "lease_start": self.lease_start.isoformat() if self.lease_start else None,
            "lease_end": self.lease_end.isoformat() if self.lease_end else None,
            "monthly_rent": float(self.monthly_rent) if self.monthly_rent else None,
            "security_deposit": float(self.security_deposit) if self.security_deposit else None,
            "status": self.status,
            "is_lease_active": self.is_lease_active,
            "tal_registered": self.tal_registered,
            "tal_registration_number": self.tal_registration_number,
        }


class RentPayment(Base):
    """Rent payment record."""
    
    __tablename__ = "rent_payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50))
    
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    status = Column(String(20), default=PaymentStatus.RECEIVED.value)
    
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="payments")
    
    def __repr__(self):
        return f"<RentPayment {self.amount} on {self.payment_date}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "property_id": str(self.property_id),
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "amount": float(self.amount) if self.amount else None,
            "payment_method": self.payment_method,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "status": self.status,
            "notes": self.notes,
        }


class MaintenanceRequest(Base):
    """Maintenance request for property."""
    
    __tablename__ = "maintenance_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("property_units.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    category = Column(String(50))
    priority = Column(String(20), default=MaintenancePriority.MEDIUM.value)
    
    status = Column(String(20), default=MaintenanceStatus.OPEN.value)
    
    assigned_contractor_id = Column(UUID(as_uuid=True))
    estimated_cost = Column(Numeric(10, 2))
    actual_cost = Column(Numeric(10, 2))
    
    requested_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    photos = Column(ARRAY(Text))
    notes = Column(Text)
    
    # Relationships
    property = relationship("Property", back_populates="maintenance_requests")
    
    def __repr__(self):
        return f"<MaintenanceRequest {self.title}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "property_id": str(self.property_id),
            "unit_id": str(self.unit_id) if self.unit_id else None,
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "estimated_cost": float(self.estimated_cost) if self.estimated_cost else None,
            "actual_cost": float(self.actual_cost) if self.actual_cost else None,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "photos": self.photos,
        }
