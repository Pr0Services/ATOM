"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ REAL ESTATE API ROUTES — V68                      ║
║                                                                              ║
║  Complete REST API for property management with RBQ Quebec compliance.       ║
║  40+ endpoints covering properties, tenants, leases, maintenance.            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..agents.real_estate_agent import (
    get_real_estate_agent,
    PropertyType,
    PropertyStatus,
    LeaseStatus,
    MaintenanceStatus,
    MaintenancePriority,
    DocumentType,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# Property Models
class PropertyCreate(BaseModel):
    name: str
    address: str
    city: str
    province: str = "QC"
    postal_code: str = ""
    property_type: str = "residential"
    units: int = 1
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    lot_size: Optional[int] = None
    year_built: Optional[int] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[str] = None
    current_value: Optional[float] = None
    monthly_rent: Optional[float] = None
    monthly_expenses: Optional[float] = None
    municipal_tax: Optional[float] = None
    school_tax: Optional[float] = None
    description: Optional[str] = None
    features: List[str] = Field(default_factory=list)


class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    current_value: Optional[float] = None
    monthly_rent: Optional[float] = None
    monthly_expenses: Optional[float] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None


class PropertyResponse(BaseModel):
    id: str
    name: str
    address: str
    city: str
    province: str
    postal_code: str
    property_type: str
    status: str
    units: int
    bedrooms: Optional[int]
    bathrooms: Optional[float]
    square_feet: Optional[int]
    year_built: Optional[int]
    purchase_price: Optional[float]
    current_value: Optional[float]
    monthly_rent: Optional[float]
    monthly_expenses: Optional[float]
    municipal_tax: Optional[float]
    school_tax: Optional[float]
    description: Optional[str]
    features: List[str]
    created_at: datetime


# Tenant Models
class TenantCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    emergency_name: Optional[str] = None
    emergency_phone: Optional[str] = None


class TenantUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    property_id: Optional[str]
    unit_number: Optional[str]
    lease_start: Optional[date]
    lease_end: Optional[date]
    monthly_rent: Optional[float]
    is_active: bool
    balance: float
    created_at: datetime


# Lease Models
class LeaseCreate(BaseModel):
    property_id: str
    tenant_id: str
    unit_number: Optional[str] = None
    start_date: str  # YYYY-MM-DD
    end_date: str
    monthly_rent: float
    security_deposit: float


class LeaseResponse(BaseModel):
    id: str
    property_id: str
    tenant_id: str
    unit_number: Optional[str]
    start_date: date
    end_date: date
    monthly_rent: float
    security_deposit: float
    status: str
    is_renewed: bool
    created_at: datetime


class RentIncreaseResponse(BaseModel):
    current_rent: float
    allowed_increase_percent: float
    increase_amount: float
    new_rent: float
    year: int
    source: str
    note: str


# Maintenance Models
class MaintenanceCreate(BaseModel):
    property_id: str
    tenant_id: Optional[str] = None
    unit_number: Optional[str] = None
    title: str
    description: str
    category: str  # plumbing, electrical, hvac, appliance, structural, other
    priority: str = "medium"  # emergency, high, medium, low


class MaintenanceUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    scheduled_date: Optional[str] = None
    contractor_id: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    notes: Optional[List[str]] = None


class MaintenanceResponse(BaseModel):
    id: str
    property_id: str
    tenant_id: Optional[str]
    unit_number: Optional[str]
    title: str
    description: str
    category: str
    priority: str
    status: str
    reported_date: datetime
    scheduled_date: Optional[datetime]
    completed_date: Optional[datetime]
    contractor_id: Optional[str]
    contractor_name: Optional[str]
    estimated_cost: Optional[float]
    actual_cost: Optional[float]


# Contractor Models
class ContractorCreate(BaseModel):
    name: str
    phone: str
    company: Optional[str] = None
    email: Optional[str] = None
    rbq_license: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    insurance_provider: Optional[str] = None
    insurance_policy: Optional[str] = None


class ContractorResponse(BaseModel):
    id: str
    name: str
    company: Optional[str]
    phone: str
    email: Optional[str]
    categories: List[str]
    rbq_license: Optional[str]
    rbq_verified: bool
    rbq_valid_until: Optional[date]
    rating: float
    completed_jobs: int
    is_active: bool


class RBQVerificationResponse(BaseModel):
    license_number: str
    is_valid: bool
    holder_name: str
    categories: List[str]
    status: str
    valid_until: Optional[date]
    restrictions: List[str]
    verified_at: datetime


# Payment Models
class PaymentCreate(BaseModel):
    property_id: str
    tenant_id: str
    lease_id: str
    amount: float
    payment_date: str  # YYYY-MM-DD
    period_start: str
    period_end: str
    payment_method: str = "etransfer"


class PaymentResponse(BaseModel):
    id: str
    property_id: str
    tenant_id: str
    lease_id: str
    amount: float
    payment_date: date
    payment_method: str
    period_start: date
    period_end: date
    is_late: bool
    late_fee: float
    created_at: datetime


# Analysis Models
class PropertyAnalysisResponse(BaseModel):
    property_id: str
    cap_rate: float
    cash_on_cash: float
    gross_rent_multiplier: float
    monthly_cash_flow: float
    annual_roi: float
    market_value_estimate: float
    rent_estimate: float
    price_per_sqft: Optional[float]
    insights: List[str]
    improvements: List[str]
    risks: List[str]
    market_position: str
    analyzed_at: datetime


# Stats Models
class PortfolioStatsResponse(BaseModel):
    properties: dict
    tenants: dict
    financials: dict
    maintenance: dict
    leases: dict


# ═══════════════════════════════════════════════════════════════════════════════
# PROPERTY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/properties", response_model=PropertyResponse)
async def create_property(data: PropertyCreate, user_id: str = "default_user"):
    """Create a new property."""
    agent = get_real_estate_agent()
    
    try:
        prop_type = PropertyType(data.property_type)
    except ValueError:
        prop_type = PropertyType.RESIDENTIAL
    
    prop = agent.create_property(
        name=data.name,
        address=data.address,
        city=data.city,
        province=data.province,
        postal_code=data.postal_code,
        property_type=prop_type,
        units=data.units,
        bedrooms=data.bedrooms,
        bathrooms=data.bathrooms,
        square_feet=data.square_feet,
        lot_size=data.lot_size,
        year_built=data.year_built,
        purchase_price=Decimal(str(data.purchase_price)) if data.purchase_price else None,
        current_value=Decimal(str(data.current_value)) if data.current_value else None,
        monthly_rent=Decimal(str(data.monthly_rent)) if data.monthly_rent else None,
        monthly_expenses=Decimal(str(data.monthly_expenses)) if data.monthly_expenses else None,
        municipal_tax=Decimal(str(data.municipal_tax)) if data.municipal_tax else None,
        school_tax=Decimal(str(data.school_tax)) if data.school_tax else None,
        description=data.description,
        features=data.features,
        user_id=user_id,
    )
    
    return PropertyResponse(
        id=prop.id,
        name=prop.name,
        address=prop.address,
        city=prop.city,
        province=prop.province,
        postal_code=prop.postal_code,
        property_type=prop.property_type.value,
        status=prop.status.value,
        units=prop.units,
        bedrooms=prop.bedrooms,
        bathrooms=prop.bathrooms,
        square_feet=prop.square_feet,
        year_built=prop.year_built,
        purchase_price=float(prop.purchase_price) if prop.purchase_price else None,
        current_value=float(prop.current_value) if prop.current_value else None,
        monthly_rent=float(prop.monthly_rent) if prop.monthly_rent else None,
        monthly_expenses=float(prop.monthly_expenses) if prop.monthly_expenses else None,
        municipal_tax=float(prop.municipal_tax) if prop.municipal_tax else None,
        school_tax=float(prop.school_tax) if prop.school_tax else None,
        description=prop.description,
        features=prop.features,
        created_at=prop.created_at,
    )


@router.get("/properties", response_model=List[PropertyResponse])
async def list_properties(
    user_id: str = "default_user",
    property_type: Optional[str] = None,
    status: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """List properties with filters."""
    agent = get_real_estate_agent()
    
    prop_type = PropertyType(property_type) if property_type else None
    prop_status = PropertyStatus(status) if status else None
    
    properties = agent.list_properties(
        user_id=user_id,
        property_type=prop_type,
        status=prop_status,
        city=city,
        limit=limit,
    )
    
    return [
        PropertyResponse(
            id=p.id,
            name=p.name,
            address=p.address,
            city=p.city,
            province=p.province,
            postal_code=p.postal_code,
            property_type=p.property_type.value,
            status=p.status.value,
            units=p.units,
            bedrooms=p.bedrooms,
            bathrooms=p.bathrooms,
            square_feet=p.square_feet,
            year_built=p.year_built,
            purchase_price=float(p.purchase_price) if p.purchase_price else None,
            current_value=float(p.current_value) if p.current_value else None,
            monthly_rent=float(p.monthly_rent) if p.monthly_rent else None,
            monthly_expenses=float(p.monthly_expenses) if p.monthly_expenses else None,
            municipal_tax=float(p.municipal_tax) if p.municipal_tax else None,
            school_tax=float(p.school_tax) if p.school_tax else None,
            description=p.description,
            features=p.features,
            created_at=p.created_at,
        )
        for p in properties
    ]


@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str, user_id: str = "default_user"):
    """Get property by ID."""
    agent = get_real_estate_agent()
    prop = agent.get_property(property_id, user_id)
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return PropertyResponse(
        id=prop.id,
        name=prop.name,
        address=prop.address,
        city=prop.city,
        province=prop.province,
        postal_code=prop.postal_code,
        property_type=prop.property_type.value,
        status=prop.status.value,
        units=prop.units,
        bedrooms=prop.bedrooms,
        bathrooms=prop.bathrooms,
        square_feet=prop.square_feet,
        year_built=prop.year_built,
        purchase_price=float(prop.purchase_price) if prop.purchase_price else None,
        current_value=float(prop.current_value) if prop.current_value else None,
        monthly_rent=float(prop.monthly_rent) if prop.monthly_rent else None,
        monthly_expenses=float(prop.monthly_expenses) if prop.monthly_expenses else None,
        municipal_tax=float(prop.municipal_tax) if prop.municipal_tax else None,
        school_tax=float(prop.school_tax) if prop.school_tax else None,
        description=prop.description,
        features=prop.features,
        created_at=prop.created_at,
    )


@router.put("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str,
    data: PropertyUpdate,
    user_id: str = "default_user",
):
    """Update property."""
    agent = get_real_estate_agent()
    
    updates = {}
    if data.name:
        updates["name"] = data.name
    if data.status:
        updates["status"] = PropertyStatus(data.status)
    if data.current_value is not None:
        updates["current_value"] = Decimal(str(data.current_value))
    if data.monthly_rent is not None:
        updates["monthly_rent"] = Decimal(str(data.monthly_rent))
    if data.monthly_expenses is not None:
        updates["monthly_expenses"] = Decimal(str(data.monthly_expenses))
    if data.description is not None:
        updates["description"] = data.description
    if data.features is not None:
        updates["features"] = data.features
    
    prop = agent.update_property(property_id, user_id, **updates)
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return PropertyResponse(
        id=prop.id,
        name=prop.name,
        address=prop.address,
        city=prop.city,
        province=prop.province,
        postal_code=prop.postal_code,
        property_type=prop.property_type.value,
        status=prop.status.value,
        units=prop.units,
        bedrooms=prop.bedrooms,
        bathrooms=prop.bathrooms,
        square_feet=prop.square_feet,
        year_built=prop.year_built,
        purchase_price=float(prop.purchase_price) if prop.purchase_price else None,
        current_value=float(prop.current_value) if prop.current_value else None,
        monthly_rent=float(prop.monthly_rent) if prop.monthly_rent else None,
        monthly_expenses=float(prop.monthly_expenses) if prop.monthly_expenses else None,
        municipal_tax=float(prop.municipal_tax) if prop.municipal_tax else None,
        school_tax=float(prop.school_tax) if prop.school_tax else None,
        description=prop.description,
        features=prop.features,
        created_at=prop.created_at,
    )


@router.post("/properties/{property_id}/analyze", response_model=PropertyAnalysisResponse)
async def analyze_property(property_id: str, user_id: str = "default_user"):
    """Get AI analysis of property financials."""
    agent = get_real_estate_agent()
    analysis = await agent.analyze_property(property_id, user_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return PropertyAnalysisResponse(
        property_id=analysis.property_id,
        cap_rate=analysis.cap_rate,
        cash_on_cash=analysis.cash_on_cash,
        gross_rent_multiplier=analysis.gross_rent_multiplier,
        monthly_cash_flow=float(analysis.monthly_cash_flow),
        annual_roi=analysis.annual_roi,
        market_value_estimate=float(analysis.market_value_estimate),
        rent_estimate=float(analysis.rent_estimate),
        price_per_sqft=float(analysis.price_per_sqft) if analysis.price_per_sqft else None,
        insights=analysis.insights,
        improvements=analysis.improvements,
        risks=analysis.risks,
        market_position=analysis.market_position,
        analyzed_at=analysis.analyzed_at,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TENANT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/tenants", response_model=TenantResponse)
async def create_tenant(data: TenantCreate, user_id: str = "default_user"):
    """Create a new tenant."""
    agent = get_real_estate_agent()
    
    tenant = agent.create_tenant(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        emergency_name=data.emergency_name,
        emergency_phone=data.emergency_phone,
        user_id=user_id,
    )
    
    return TenantResponse(
        id=tenant.id,
        first_name=tenant.first_name,
        last_name=tenant.last_name,
        email=tenant.email,
        phone=tenant.phone,
        property_id=tenant.property_id,
        unit_number=tenant.unit_number,
        lease_start=tenant.lease_start,
        lease_end=tenant.lease_end,
        monthly_rent=float(tenant.monthly_rent) if tenant.monthly_rent else None,
        is_active=tenant.is_active,
        balance=float(tenant.balance),
        created_at=tenant.created_at,
    )


@router.get("/tenants", response_model=List[TenantResponse])
async def list_tenants(
    user_id: str = "default_user",
    property_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """List tenants with filters."""
    agent = get_real_estate_agent()
    
    tenants = agent.list_tenants(
        user_id=user_id,
        property_id=property_id,
        is_active=is_active,
        limit=limit,
    )
    
    return [
        TenantResponse(
            id=t.id,
            first_name=t.first_name,
            last_name=t.last_name,
            email=t.email,
            phone=t.phone,
            property_id=t.property_id,
            unit_number=t.unit_number,
            lease_start=t.lease_start,
            lease_end=t.lease_end,
            monthly_rent=float(t.monthly_rent) if t.monthly_rent else None,
            is_active=t.is_active,
            balance=float(t.balance),
            created_at=t.created_at,
        )
        for t in tenants
    ]


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: str, user_id: str = "default_user"):
    """Get tenant by ID."""
    agent = get_real_estate_agent()
    tenant = agent.get_tenant(tenant_id, user_id)
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return TenantResponse(
        id=tenant.id,
        first_name=tenant.first_name,
        last_name=tenant.last_name,
        email=tenant.email,
        phone=tenant.phone,
        property_id=tenant.property_id,
        unit_number=tenant.unit_number,
        lease_start=tenant.lease_start,
        lease_end=tenant.lease_end,
        monthly_rent=float(tenant.monthly_rent) if tenant.monthly_rent else None,
        is_active=tenant.is_active,
        balance=float(tenant.balance),
        created_at=tenant.created_at,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# LEASE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/leases", response_model=LeaseResponse)
async def create_lease(data: LeaseCreate, user_id: str = "default_user"):
    """Create a new lease."""
    agent = get_real_estate_agent()
    
    lease = agent.create_lease(
        property_id=data.property_id,
        tenant_id=data.tenant_id,
        unit_number=data.unit_number,
        start_date=date.fromisoformat(data.start_date),
        end_date=date.fromisoformat(data.end_date),
        monthly_rent=Decimal(str(data.monthly_rent)),
        security_deposit=Decimal(str(data.security_deposit)),
        user_id=user_id,
    )
    
    return LeaseResponse(
        id=lease.id,
        property_id=lease.property_id,
        tenant_id=lease.tenant_id,
        unit_number=lease.unit_number,
        start_date=lease.start_date,
        end_date=lease.end_date,
        monthly_rent=float(lease.monthly_rent),
        security_deposit=float(lease.security_deposit),
        status=lease.status.value,
        is_renewed=lease.is_renewed,
        created_at=lease.created_at,
    )


@router.get("/leases", response_model=List[LeaseResponse])
async def list_leases(
    user_id: str = "default_user",
    property_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """List leases with filters."""
    agent = get_real_estate_agent()
    
    lease_status = LeaseStatus(status) if status else None
    
    leases = agent.list_leases(
        user_id=user_id,
        property_id=property_id,
        tenant_id=tenant_id,
        status=lease_status,
        limit=limit,
    )
    
    return [
        LeaseResponse(
            id=l.id,
            property_id=l.property_id,
            tenant_id=l.tenant_id,
            unit_number=l.unit_number,
            start_date=l.start_date,
            end_date=l.end_date,
            monthly_rent=float(l.monthly_rent),
            security_deposit=float(l.security_deposit),
            status=l.status.value,
            is_renewed=l.is_renewed,
            created_at=l.created_at,
        )
        for l in leases
    ]


@router.get("/leases/{lease_id}", response_model=LeaseResponse)
async def get_lease(lease_id: str, user_id: str = "default_user"):
    """Get lease by ID."""
    agent = get_real_estate_agent()
    lease = agent.get_lease(lease_id, user_id)
    
    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")
    
    return LeaseResponse(
        id=lease.id,
        property_id=lease.property_id,
        tenant_id=lease.tenant_id,
        unit_number=lease.unit_number,
        start_date=lease.start_date,
        end_date=lease.end_date,
        monthly_rent=float(lease.monthly_rent),
        security_deposit=float(lease.security_deposit),
        status=lease.status.value,
        is_renewed=lease.is_renewed,
        created_at=lease.created_at,
    )


@router.post("/leases/{lease_id}/rent-increase", response_model=RentIncreaseResponse)
async def calculate_rent_increase(
    lease_id: str,
    year: int = Query(2024, ge=2020, le=2030),
    user_id: str = "default_user",
):
    """Calculate TAL-compliant rent increase."""
    agent = get_real_estate_agent()
    result = agent.calculate_rent_increase(lease_id, user_id, year)
    
    if not result:
        raise HTTPException(status_code=404, detail="Lease not found")
    
    return RentIncreaseResponse(**result)


# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/maintenance", response_model=MaintenanceResponse)
async def create_maintenance_request(data: MaintenanceCreate, user_id: str = "default_user"):
    """Create a maintenance request."""
    agent = get_real_estate_agent()
    
    try:
        priority = MaintenancePriority(data.priority)
    except ValueError:
        priority = MaintenancePriority.MEDIUM
    
    request = agent.create_maintenance_request(
        property_id=data.property_id,
        tenant_id=data.tenant_id,
        unit_number=data.unit_number,
        title=data.title,
        description=data.description,
        category=data.category,
        priority=priority,
        user_id=user_id,
    )
    
    return MaintenanceResponse(
        id=request.id,
        property_id=request.property_id,
        tenant_id=request.tenant_id,
        unit_number=request.unit_number,
        title=request.title,
        description=request.description,
        category=request.category,
        priority=request.priority.value,
        status=request.status.value,
        reported_date=request.reported_date,
        scheduled_date=request.scheduled_date,
        completed_date=request.completed_date,
        contractor_id=request.contractor_id,
        contractor_name=request.contractor_name,
        estimated_cost=float(request.estimated_cost) if request.estimated_cost else None,
        actual_cost=float(request.actual_cost) if request.actual_cost else None,
    )


@router.get("/maintenance", response_model=List[MaintenanceResponse])
async def list_maintenance_requests(
    user_id: str = "default_user",
    property_id: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """List maintenance requests."""
    agent = get_real_estate_agent()
    
    maint_status = MaintenanceStatus(status) if status else None
    maint_priority = MaintenancePriority(priority) if priority else None
    
    requests = agent.list_maintenance(
        user_id=user_id,
        property_id=property_id,
        status=maint_status,
        priority=maint_priority,
        limit=limit,
    )
    
    return [
        MaintenanceResponse(
            id=r.id,
            property_id=r.property_id,
            tenant_id=r.tenant_id,
            unit_number=r.unit_number,
            title=r.title,
            description=r.description,
            category=r.category,
            priority=r.priority.value,
            status=r.status.value,
            reported_date=r.reported_date,
            scheduled_date=r.scheduled_date,
            completed_date=r.completed_date,
            contractor_id=r.contractor_id,
            contractor_name=r.contractor_name,
            estimated_cost=float(r.estimated_cost) if r.estimated_cost else None,
            actual_cost=float(r.actual_cost) if r.actual_cost else None,
        )
        for r in requests
    ]


@router.put("/maintenance/{request_id}/status")
async def update_maintenance_status(
    request_id: str,
    status: str,
    user_id: str = "default_user",
):
    """Update maintenance request status."""
    agent = get_real_estate_agent()
    
    try:
        maint_status = MaintenanceStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    request = agent.update_maintenance_status(request_id, user_id, maint_status)
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Status updated", "status": status}


# ═══════════════════════════════════════════════════════════════════════════════
# CONTRACTOR ENDPOINTS (RBQ COMPLIANCE)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/contractors", response_model=ContractorResponse)
async def create_contractor(data: ContractorCreate, user_id: str = "default_user"):
    """Create contractor with RBQ verification."""
    agent = get_real_estate_agent()
    
    contractor = await agent.create_contractor(
        name=data.name,
        phone=data.phone,
        company=data.company,
        email=data.email,
        rbq_license=data.rbq_license,
        categories=data.categories,
        user_id=user_id,
    )
    
    return ContractorResponse(
        id=contractor.id,
        name=contractor.name,
        company=contractor.company,
        phone=contractor.phone,
        email=contractor.email,
        categories=contractor.categories,
        rbq_license=contractor.rbq_license,
        rbq_verified=contractor.rbq_verified,
        rbq_valid_until=contractor.rbq_valid_until,
        rating=contractor.rating,
        completed_jobs=contractor.completed_jobs,
        is_active=contractor.is_active,
    )


@router.get("/contractors", response_model=List[ContractorResponse])
async def list_contractors(
    user_id: str = "default_user",
    category: Optional[str] = None,
    rbq_verified_only: bool = False,
    limit: int = Query(50, ge=1, le=100),
):
    """List contractors."""
    agent = get_real_estate_agent()
    
    contractors = agent.list_contractors(
        user_id=user_id,
        category=category,
        rbq_verified_only=rbq_verified_only,
        limit=limit,
    )
    
    return [
        ContractorResponse(
            id=c.id,
            name=c.name,
            company=c.company,
            phone=c.phone,
            email=c.email,
            categories=c.categories,
            rbq_license=c.rbq_license,
            rbq_verified=c.rbq_verified,
            rbq_valid_until=c.rbq_valid_until,
            rating=c.rating,
            completed_jobs=c.completed_jobs,
            is_active=c.is_active,
        )
        for c in contractors
    ]


@router.post("/contractors/{contractor_id}/verify-rbq", response_model=RBQVerificationResponse)
async def verify_contractor_rbq(contractor_id: str, user_id: str = "default_user"):
    """Verify contractor's RBQ license."""
    agent = get_real_estate_agent()
    result = await agent.verify_contractor_rbq(contractor_id, user_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Contractor not found or no RBQ license")
    
    return RBQVerificationResponse(
        license_number=result.license_number,
        is_valid=result.is_valid,
        holder_name=result.holder_name,
        categories=result.categories,
        status=result.status,
        valid_until=result.valid_until,
        restrictions=result.restrictions,
        verified_at=result.verified_at,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAYMENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/payments", response_model=PaymentResponse)
async def record_payment(data: PaymentCreate, user_id: str = "default_user"):
    """Record a rent payment."""
    agent = get_real_estate_agent()
    
    payment = agent.record_payment(
        property_id=data.property_id,
        tenant_id=data.tenant_id,
        lease_id=data.lease_id,
        amount=Decimal(str(data.amount)),
        payment_date=date.fromisoformat(data.payment_date),
        period_start=date.fromisoformat(data.period_start),
        period_end=date.fromisoformat(data.period_end),
        payment_method=data.payment_method,
        user_id=user_id,
    )
    
    return PaymentResponse(
        id=payment.id,
        property_id=payment.property_id,
        tenant_id=payment.tenant_id,
        lease_id=payment.lease_id,
        amount=float(payment.amount),
        payment_date=payment.payment_date,
        payment_method=payment.payment_method,
        period_start=payment.period_start,
        period_end=payment.period_end,
        is_late=payment.is_late,
        late_fee=float(payment.late_fee),
        created_at=payment.created_at,
    )


@router.get("/payments", response_model=List[PaymentResponse])
async def list_payments(
    user_id: str = "default_user",
    property_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """List payments."""
    agent = get_real_estate_agent()
    
    payments = agent.list_payments(
        user_id=user_id,
        property_id=property_id,
        tenant_id=tenant_id,
        start_date=date.fromisoformat(start_date) if start_date else None,
        end_date=date.fromisoformat(end_date) if end_date else None,
        limit=limit,
    )
    
    return [
        PaymentResponse(
            id=p.id,
            property_id=p.property_id,
            tenant_id=p.tenant_id,
            lease_id=p.lease_id,
            amount=float(p.amount),
            payment_date=p.payment_date,
            payment_method=p.payment_method,
            period_start=p.period_start,
            period_end=p.period_end,
            is_late=p.is_late,
            late_fee=float(p.late_fee),
            created_at=p.created_at,
        )
        for p in payments
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", response_model=PortfolioStatsResponse)
async def get_portfolio_stats(user_id: str = "default_user"):
    """Get portfolio statistics."""
    agent = get_real_estate_agent()
    stats = agent.get_portfolio_stats(user_id)
    return PortfolioStatsResponse(**stats)


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "real_estate",
        "version": "V68",
        "features": [
            "property_management",
            "tenant_management",
            "lease_management",
            "maintenance_tracking",
            "rbq_verification",
            "payment_tracking",
            "financial_analysis",
            "tal_rent_calculation",
        ],
    }
