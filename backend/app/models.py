from datetime import datetime
from sqlalchemy import Column, Text, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base
    
# Define the User and Assignment models
# These models represent the database tables for users and assignments
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, server_default=func.now())
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    assignments= relationship('Assignment', back_populates='owner') # Defines one owner to many assignments

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, server_default=func.now())
    title = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False) 
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False) # foreign key to link assignment to the user
    owner = relationship('User', back_populates='assignments') # Defines many assignments to one owner 