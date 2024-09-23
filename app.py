from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import datetime as dt
import os 
import psycopg2
from psycopg2.errors import DuplicateTable
import os
import uvicorn

IS_DB_INITIALIZED = False

class Transaction(BaseModel):
    amt: float
    acc: str
    cat: str


print("fast api initiated")
def getCon():
    return psycopg2.connect(database=os.getenv("DB_DB","postgres"), user=os.getenv("DB_USER","postgres"), password=os.getenv("DB_PASS","pass"), host=os.getenv("DB_HOST","127.0.0.1"), port=os.getenv("DB_PORT",5432))

def setupDatabase():
    global IS_DB_INITIALIZED
    print("Connecting db...")
    connection = getCon()
    print("Connected db...")
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE table ACCOUNT (	amt numeric, acc text, category text);")
        connection.commit()
        IS_DB_INITIALIZED = True
    except DuplicateTable as d:
        print("table already found")
        IS_DB_INITIALIZED = True
    except Exception as e:
        print("Failed while exexuting db query: ", str(e))
    finally:
        connection.close()


app = FastAPI()
app_ls = ["FAST_API_HOST","FAST_API_PORT","DB_HOST","DB_PORT","DB_PASS","DB_DB","DB_USER","FAST_API_CONT","NET_NAME","FAST_API_IMG","DB_IMG"]
os.system("ls -al")
for ky in app_ls:
    print(ky,os.getenv(ky,"not found"))


@app.get("/")
def hello():
    if IS_DB_INITIALIZED == False:
        setupDatabase()
    file = open("user.html","r")
    data = file.read()
    data = data.replace("$__API_PORT",os.getenv("FAST_API_PORT","9128"))
    return HTMLResponse(content=data, status_code=200)
    
@app.post("/save")
async def storeData(t1: Transaction):
    try:
        connection = getCon()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ACCOUNT VALUES({},'{}','{}')".format(t1.amt, t1.acc, t1.cat))
        connection.commit()
        connection.close()
        return {"success": True}
    except Exception as e:
        return {"success":False, "error": e}


@app.get("/allData")
async def getAllData():
    try:
        connection = getCon()
        cursor = connection.cursor()
        cursor.execute("select ROW_NUMBER() OVER (order by amt) as \"rm\", amt, acc, category from account order by 1 desc;")
        record1 = cursor.fetchall()
        cursor.execute("""with a as ( select acc, sum(amt) as "at" from account group by 1) select ROW_NUMBER() OVER (order by a.acc) as "rm", a.acc, a.at from a order by 1 desc;""")
        record2 = cursor.fetchall()
        connection.close()
        d1 = []
        print(record1)
        for k in record1:
            l = list(map(lambda x: str(x), k))
            l = "$" + "$".join(l)
            d1.append(l)
        print(d1)
        d2 = []
        for k in record2:
            l = list(map(lambda x: str(x), k))
            l = "$" + "$".join(l)
            d2.append(l)
        print(d2)
        print("all data",d1)
        print("agg data", d2)
        return {"success": True, "all": d1, "agg": d2}
    except Exception as e:
        print("error : ", e)
        return {"success":False, "error": e}


@app.get("/view")
async def view():
    if IS_DB_INITIALIZED == False:
        setupDatabase()
    file = open("data.html","r")
    data = file.read()
    data = data.replace("$__API_PORT",os.getenv("FAST_API_PORT","9128"))
    return HTMLResponse(content=data, status_code=200)


if __name__ == "__main__":
    print("hel1", int(os.getenv("FAST_API_PORT",9128)))
    uvicorn.run(app, host=os.getenv("FAST_API_HOST","127.0.0.1"), port=int(os.getenv("FAST_API_PORT",9128)))