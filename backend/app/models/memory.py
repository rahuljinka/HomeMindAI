from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database.session import Base

class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="houses")
    rooms = relationship("Room", back_populates="house", cascade="all, delete-orphan")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id"))
    name = Column(String, nullable=False)
    description = Column(Text)

    user = relationship("User", back_populates="rooms")
    house = relationship("House", back_populates="rooms")
    furniture = relationship("Furniture", back_populates="room", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="room")

class Furniture(Base):
    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)

    room = relationship("Room", back_populates="furniture")
    containers = relationship("Container", back_populates="furniture", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="furniture")

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    furniture_id = Column(Integer, ForeignKey("furniture.id"), nullable=False)
    name = Column(String, nullable=False)

    furniture = relationship("Furniture", back_populates="containers")
    locations = relationship("Location", back_populates="container")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    furniture_id = Column(Integer, ForeignKey("furniture.id"))
    container_id = Column(Integer, ForeignKey("containers.id"))

    room = relationship("Room", back_populates="locations")
    furniture = relationship("Furniture", back_populates="locations")
    container = relationship("Container", back_populates="locations")
    objects = relationship("StoredObject", back_populates="current_location")

class StoredObject(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(Text)
    current_location_id = Column(Integer, ForeignKey("locations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="objects")
    current_location = relationship("Location", back_populates="objects")
    history = relationship("MemoryHistory", back_populates="stored_object", cascade="all, delete-orphan")
    aliases = relationship("ObjectAlias", back_populates="stored_object", cascade="all, delete-orphan")
    photos = relationship("ObjectPhoto", back_populates="stored_object", cascade="all, delete-orphan")
    embedding = relationship("ObjectEmbedding", back_populates="stored_object", uselist=False, cascade="all, delete-orphan")

class ObjectAlias(Base):
    __tablename__ = "object_aliases"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    alias = Column(String, nullable=False)

    stored_object = relationship("StoredObject", back_populates="aliases")

class ObjectPhoto(Base):
    __tablename__ = "object_photos"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stored_object = relationship("StoredObject", back_populates="photos")

class ObjectEmbedding(Base):
    __tablename__ = "object_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    embedding = Column(Vector(1536))  # Default size for OpenAI text-embedding-3-small
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stored_object = relationship("StoredObject", back_populates="embedding")

class MemoryHistory(Base):
    __tablename__ = "memory_history"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    previous_location = Column(Text)
    new_location = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(Text)

    stored_object = relationship("StoredObject", back_populates="history")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False) # user or assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")
