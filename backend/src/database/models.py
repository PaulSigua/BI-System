from sqlalchemy import Column, Integer, String, VARBINARY, Boolean, DateTime, UniqueConstraint, ForeignKey, Table
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from .connection import Base
import datetime

# Association tables
tbl_user_roles = Table(
    'UserRoles', Base.metadata,
    Column('UserId', Integer, ForeignKey('Users.UserId'), primary_key=True),
    Column('RoleId', Integer, ForeignKey('Roles.RoleId'), primary_key=True),
    Column('AssignedAt', DateTime, default=datetime.datetime.utcnow)
)

tbl_role_reports = Table(
    'RolePowerBIReports', Base.metadata,
    Column('RoleId', Integer, ForeignKey('Roles.RoleId', ondelete='CASCADE'), primary_key=True),
    Column('ReportId', Integer, ForeignKey('PowerBIReports.ReportId', ondelete='CASCADE'), primary_key=True),
    Column('AssignedAt', DateTime, default=datetime.datetime.utcnow)
)

class Role(Base):
    __tablename__ = 'Roles'
    RoleId = Column(Integer, primary_key=True, index=True)
    RoleName = Column(String(50), unique=True, nullable=False)
    Description = Column(String(200))
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    users = relationship('User', secondary=tbl_user_roles, back_populates='roles')
    reports = relationship('PowerBIReport', secondary=tbl_role_reports, back_populates='roles')

class User(Base):
    __tablename__ = 'Users'
    UserId = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    PasswordHash = Column(String(128), nullable=False)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    roles = relationship('Role', secondary=tbl_user_roles, back_populates='users')
    reports = relationship('PowerBIReport', back_populates='owner')

class PowerBIReport(Base):
    __tablename__ = 'PowerBIReports'
    ReportId = Column(Integer, primary_key=True, index=True)
    ReportName = Column(String(100), nullable=False)
    ReportUrl = Column(String(500), nullable=False)
    OwnerId = Column(Integer, ForeignKey('Users.UserId'), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship('User', back_populates='reports')
    roles = relationship('Role', secondary=tbl_role_reports, back_populates='reports')

class RefreshToken(Base):
    __tablename__ = 'RefreshTokens'
    TokenId = Column(UNIQUEIDENTIFIER, primary_key=True)
    UserId = Column(Integer, ForeignKey('Users.UserId'), nullable=False)
    Token = Column(String(200), unique=True, nullable=False)
    ExpiresAt = Column(DateTime, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    RevokedAt = Column(DateTime)
    ReplacedByToken = Column(String(200))
    user = relationship('User')