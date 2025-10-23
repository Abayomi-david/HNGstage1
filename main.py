from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

import models, schemas, utils
from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="String Analyzer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create/Analyze String
@app.post("/strings", response_model=schemas.StringResponse, status_code=201)
def create_string(payload: schemas.StringRequest, db: Session = Depends(get_db)):
    if not isinstance(payload.value, str):
        raise HTTPException(status_code=422, detail='"value" must be a string')

    props = utils.compute_properties(payload.value)
    existing = db.query(models.StringModel).filter_by(id=props["sha256_hash"]).first()
    if existing:
        raise HTTPException(status_code=409, detail="String already exists")

    db_obj = models.StringModel(
        id=props["sha256_hash"],
        value=payload.value,
        properties=json.dumps(props),
        created_at=datetime.utcnow(),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return {
        "id": db_obj.id,
        "value": db_obj.value,
        "properties": props,
        "created_at": db_obj.created_at,
    }


#  Get Specific String
@app.get("/strings/{string_value}", response_model=schemas.StringResponse)
def get_string(string_value: str, db: Session = Depends(get_db)):
    sha = utils.compute_properties(string_value)["sha256_hash"]
    db_obj = db.query(models.StringModel).filter_by(id=sha).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="String not found")

    return {
        "id": db_obj.id,
        "value": db_obj.value,
        "properties": json.loads(db_obj.properties),
        "created_at": db_obj.created_at,
    }


#  Get All Strings (with filters)
@app.get("/strings", response_model=schemas.FilterResponse)
def list_strings(
    is_palindrome: bool = Query(None),
    min_length: int = Query(None),
    max_length: int = Query(None),
    word_count: int = Query(None),
    contains_character: str = Query(None),
    db: Session = Depends(get_db),
):
    all_data = db.query(models.StringModel).all()
    results = []

    for item in all_data:
        props = json.loads(item.properties)

        if is_palindrome is not None and props["is_palindrome"] != is_palindrome:
            continue
        if min_length is not None and props["length"] < min_length:
            continue
        if max_length is not None and props["length"] > max_length:
            continue
        if word_count is not None and props["word_count"] != word_count:
            continue
        if contains_character and contains_character not in props["character_frequency_map"]:
            continue

        results.append(
            {
                "id": item.id,
                "value": item.value,
                "properties": props,
                "created_at": item.created_at,
            }
        )

    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character,
    }

    return {"data": results, "count": len(results), "filters_applied": filters_applied}


# Natural Language Filtering
@app.get("/strings/filter-by-natural-language", response_model=schemas.NaturalLangResponse)
def filter_by_natural_language(query: str, db: Session = Depends(get_db)):
    parsed = utils.parse_natural_language(query)
    if not parsed:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    filters = parsed["parsed_filters"]
    all_data = db.query(models.StringModel).all()
    results = []

    for item in all_data:
        props = json.loads(item.properties)

        if "is_palindrome" in filters and props["is_palindrome"] != filters["is_palindrome"]:
            continue
        if "min_length" in filters and props["length"] < filters["min_length"]:
            continue
        if "word_count" in filters and props["word_count"] != filters["word_count"]:
            continue
        if "contains_character" in filters and filters["contains_character"] not in props["character_frequency_map"]:
            continue

        results.append(
            {
                "id": item.id,
                "value": item.value,
                "properties": props,
                "created_at": item.created_at,
            }
        )

    return {"data": results, "count": len(results), "interpreted_query": parsed}


#  Delete String
@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str, db: Session = Depends(get_db)):
    sha = utils.compute_properties(string_value)["sha256_hash"]
    db_obj = db.query(models.StringModel).filter_by(id=sha).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="String not found")

    db.delete(db_obj)
    db.commit()
    return None


#  Health Check
@app.get("/health")
def health():
    return {"status": "ok"}
