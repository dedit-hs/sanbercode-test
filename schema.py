from pydantic import BaseModel

class Nasabah(BaseModel):
    nama: str
    nik: str
    no_hp: str

    class Config:
        orm_mode = True


class Rekening(BaseModel):
    no_rekening: str
    saldo: int
    nasabah: str

    class Config:
        orm_mode = True


class Transaksi(BaseModel):
    nominal: int
    rekening: str

    class Config:
        orm_mode = True


class GetTransaksi(BaseModel):
    created_at: str
    rekening: str
    nominal: int

    class Config:
        orm_mode = True