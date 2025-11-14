import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI(title="EFMODE API", description="Backend for EFMODE fashion brand website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utilities
class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        try:
            return str(ObjectId(v))
        except Exception:
            raise ValueError("Invalid ObjectId")


# Schemas
from schemas import (
    Product, Collection, Review, ContactMessage, Order, Booking, GalleryItem
)

# Health
@app.get("/")
def read_root():
    return {"message": "EFMODE API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Catalog endpoints
@app.get("/api/products", response_model=List[Product])
def list_products():
    docs = get_documents("product")
    # convert ObjectId to str for images list remains same
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/products")
def create_product(product: Product):
    _id = create_document("product", product)
    return {"id": _id}

@app.get("/api/collections", response_model=List[Collection])
def list_collections():
    docs = get_documents("collection")
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/collections")
def create_collection(col: Collection):
    _id = create_document("collection", col)
    return {"id": _id}

# Reviews
@app.get("/api/reviews", response_model=List[Review])
def list_reviews():
    docs = get_documents("review")
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/reviews")
def create_review(review: Review):
    _id = create_document("review", review)
    return {"id": _id}

# Gallery
@app.get("/api/gallery", response_model=List[GalleryItem])
def list_gallery():
    docs = get_documents("galleryitem")
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/gallery")
def add_gallery(item: GalleryItem):
    _id = create_document("galleryitem", item)
    return {"id": _id}

# Contact
@app.post("/api/contact")
def contact(msg: ContactMessage):
    _id = create_document("contactmessage", msg)
    return {"id": _id, "status": "received"}

# Orders
@app.post("/api/orders")
def create_order(order: Order):
    _id = create_document("order", order)
    return {"id": _id, "status": "confirmed"}

# Tailoring bookings
@app.post("/api/bookings")
def create_booking(booking: Booking):
    _id = create_document("booking", booking)
    return {"id": _id, "status": "scheduled"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
