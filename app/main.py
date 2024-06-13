from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import database, models

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response
from pydantic import BaseModel

class CountryConfigCreate(BaseModel):
    country_code: str
    business_name: str
    registration_number: str
    additional_details: str = None

class CountryConfigUpdate(BaseModel):
    business_name: str = None
    registration_number: str = None
    additional_details: str = None

# CRUD operations
@app.post("/create_configuration", response_model=models.CountryConfig)
def create_configuration(config: CountryConfigCreate, db: Session = Depends(get_db)):
    db_config = models.CountryConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.get("/get_configuration/{country_code}", response_model=models.CountryConfig)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    config = db.query(models.CountryConfig).filter(models.CountryConfig.country_code == country_code).first()
    if config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@app.put("/update_configuration/{country_code}", response_model=models.CountryConfig)
def update_configuration(country_code: str, config: CountryConfigUpdate, db: Session = Depends(get_db)):
    db_config = db.query(models.CountryConfig).filter(models.CountryConfig.country_code == country_code).first()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    for field, value in config.dict(exclude_unset=True).items():
        setattr(db_config, field, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config

@app.delete("/delete_configuration/{country_code}", response_model=dict)
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = db.query(models.CountryConfig).filter(models.CountryConfig.country_code == country_code).first()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db.delete(db_config)
    db.commit()
    return {"message": "Configuration deleted successfully"}
