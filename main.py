import os
from random import randint
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
import shortuuid
from schema import Nasabah as SchemaNasabah
from schema import Transaksi as SchemaTransaksi
from schema import GetTransaksi
from models import Nasabah as NasabahModel
from models import Nasabah
from models import Rekening as RekeningModel
from models import Rekening
from models import Transaksi as TransaksiModel

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=f'postgresql+psycopg2://{os.environ["PGUSER"]}:{os.environ["PGPASSWORD"]}@db:{os.environ["PGPORT"]}/{os.environ["PGDATABASE"]}')

@app.get("/")
async def root():
    return {"hello": "Saya Dedit"}


def get_nasabah_by_nik(nik: int):
    return db.session.query(Nasabah).filter(Nasabah.nik == nik).first()


def get_nasabah_by_hp(no_hp: int):
    return db.session.query(Nasabah).filter(Nasabah.no_hp == no_hp).first()


@app.post("/daftar", status_code=201)
async def tambah_nasabah(nasabah: SchemaNasabah, response: Response):
    db_nasabah = NasabahModel(id=shortuuid.uuid(nasabah.nik), nama=nasabah.nama, nik=nasabah.nik, no_hp=nasabah.no_hp)
    get_rek = '404'+''.join(["{}".format(randint(0, 9)) for num in range(0, 7)])
    db_rekening = RekeningModel(id=shortuuid.uuid(get_rek), no_rekening=get_rek, saldo=0, nasabah=shortuuid.uuid(nasabah.nik))
    cek_nik = get_nasabah_by_nik(nasabah.nik)
    cek_hp = get_nasabah_by_hp(nasabah.no_hp)
    if cek_nik:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "NIK sudah terdaftar."}

    
    if cek_hp:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "No HP sudah terdaftar."}

    db.session.add(db_nasabah)
    db.session.add(db_rekening)
    db.session.commit()
    return {
        "message": "registrasi berhasil",
        "data": {
            "no_rekening": get_rek,
            "saldo": 0
        }
    }


def get_rekening(no_rek: str):
    return db.session.query(Rekening).filter(Rekening.no_rekening == no_rek).first()


@app.post("/tabung", status_code=201)
async def nasabah_menabung(transaksi: SchemaTransaksi, response: Response):
    cek_rekening = get_rekening(transaksi.rekening)
    if not cek_rekening:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "No rekening salah."}
    cek_rekening.saldo += transaksi.nominal
    db_transaksi = TransaksiModel(id=shortuuid.uuid(), kode_transaksi="C", nominal=transaksi.nominal, rekening=cek_rekening.id)
    db.session.add(db_transaksi)
    db.session.commit()
    return {
        "message": "Tabungan berhasil disimpan.",
        "data": {
            "saldo": cek_rekening.saldo
        }
    }


@app.post("/tarik", status_code=201)
async def nasabah_menarik_tabungan(transaksi: SchemaTransaksi, response:Response):
    cek_rekening = get_rekening(transaksi.rekening)
    if not cek_rekening:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "No rekening salah"}
    
    if cek_rekening.saldo < transaksi.nominal:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "Saldo tidak mencukupi."}
    
    cek_rekening.saldo -= transaksi.nominal
    db_transaksi = TransaksiModel(id=shortuuid.uuid(), kode_transaksi="D", nominal=transaksi.nominal, rekening=cek_rekening.id)
    db.session.add(db_transaksi)
    db.session.commit()
    return {
        "message": "Tabungan berhasil ditarik.",
        "data": {
            "saldo": cek_rekening.saldo
        }
    }


@app.get("/saldo/{no_rek}", status_code=200)
async def get_saldo(no_rek: str, response:Response):
    cek_rek = get_rekening(no_rek)
    if not cek_rek:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "No rekening tidak ditemukan."}
    return {
        "message": "Berhasil.",
        "saldo": cek_rek.saldo
    }


@app.get("/mutasi/{no_rek}", status_code=200)
async def get_saldo(no_rek: str, response: Response):
    cek_rek = get_rekening(no_rek)
    transaksi = db.session.query(TransaksiModel).filter(TransaksiModel.rekening == cek_rek.id).all()
    if not cek_rek:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "No rekening tidak ditemukan."}
    if not transaksi:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {"remark": "Tidak ada history transaksi."}
    
    semua_transaksi = []
    for item in transaksi:
        semua_transaksi.append({
            "waktu": item.created_at,
            "kode_transaksi": item.kode_transaksi,
            "rekening": cek_rek.no_rekening,
            "nominal": item.nominal
        })
    return semua_transaksi
