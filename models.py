from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Nasabah(Base):
    __tablename__ = "nasabah"
    id = Column(String, primary_key=True, index=True)
    nama = Column(String)
    nik = Column(String)
    no_hp = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rekening = relationship("Rekening", back_populates="nasabah_id")


class Rekening(Base):
    __tablename__ = "rekening"
    id = Column(String, primary_key=True)
    no_rekening = Column(String)
    saldo = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    nasabah = Column(String, ForeignKey("nasabah.id"))

    nasabah_id = relationship("Nasabah", back_populates="rekening")
    transaksi = relationship("Transaksi", back_populates="rekening_id")


class Transaksi(Base):
    __tablename__ = "transaksi"
    id = Column(String, primary_key=True)
    kode_transaksi = Column(String)
    nominal = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    rekening = Column(String, ForeignKey("rekening.id"))

    rekening_id = relationship("Rekening", back_populates="transaksi")
