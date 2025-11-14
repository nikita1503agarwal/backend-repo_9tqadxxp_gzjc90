"""
Database Schemas for EFMODE

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name (e.g., Product -> "product").
"""
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# Core catalog
class Product(BaseModel):
    title: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Long description")
    price: float = Field(..., ge=0, description="Price in USD")
    category: str = Field(..., description="Category or collection name")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    sizes: List[str] = Field(default_factory=lambda: ["XS","S","M","L","XL"], description="Available sizes")
    fabrics: List[str] = Field(default_factory=list, description="Fabric options / details")
    in_stock: bool = Field(True, description="Availability flag")
    featured: bool = Field(False, description="Show on homepage")

class Collection(BaseModel):
    name: str
    description: Optional[str] = None
    banner: Optional[str] = None

# Customer interactions
class Review(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    product_id: Optional[str] = Field(None, description="Optional product reference")

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str

class OrderItem(BaseModel):
    product_id: str
    title: str
    size: Optional[str] = None
    quantity: int = Field(1, ge=1)
    price: float

class Order(BaseModel):
    customer_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    items: List[OrderItem]
    total: float = Field(..., ge=0)
    notes: Optional[str] = None

class Booking(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service_type: str = Field(..., description="Tailoring | Custom Design | Alterations")
    preferred_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    preferred_time: Optional[str] = Field(None, description="HH:MM")
    measurements: Optional[dict] = None
    notes: Optional[str] = None

class GalleryItem(BaseModel):
    image_url: str
    caption: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

# Keep an example User for potential future use
class User(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
