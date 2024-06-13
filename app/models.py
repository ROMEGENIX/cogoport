from sqlalchemy import Column, Integer, String
from .database import Base

class CountryConfig(Base):
    __tablename__ = 'country_config'

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, index=True)
    business_name = Column(String)
    registration_number = Column(String)
    additional_details = Column(String)
