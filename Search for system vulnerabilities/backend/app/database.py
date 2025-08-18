from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os

from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    scans = relationship("Scan", back_populates="user")
    reports = relationship("Report", back_populates="user")

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_url = Column(String(500), nullable=False)
    scan_type = Column(String(50), nullable=False)  # full, quick, custom
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=1)  # 1=normal, 2=premium, 3=urgent
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="scans")
    vulnerabilities = relationship("Vulnerability", back_populates="scan")
    reports = relationship("Report", back_populates="scan")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    cve_id = Column(String(50), nullable=True)
    cvss_score = Column(Float, nullable=True)
    scanner_name = Column(String(100), nullable=False)  # nmap, nuclei, zap, etc.
    payload = Column(Text, nullable=True)
    location = Column(String(500), nullable=True)
    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    scan = relationship("Scan", back_populates="vulnerabilities")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    report_type = Column(String(20), nullable=False)  # pdf, excel, json
    file_path = Column(String(500), nullable=True)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")
    scan = relationship("Scan", back_populates="reports")

class ScanLog(Base):
    __tablename__ = "scan_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(20), default="info")  # info, warning, error
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    scan = relationship("Scan")
