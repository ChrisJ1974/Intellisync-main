import os
import pyodbc 
import struct

from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Revenue(BaseModel):
    year: int
    grossrevenue: float
    netrevenue: float
    beginninginventory: float
    purchases: float
    endinginventory: float
    grossrevenue: float
    sellingexpenses: float
    adminexpenses: float
    RDexpenses: float
    depAm:  float
    intIncome: float
    intExpense: float
    
connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

app = FastAPI()


@app.get("/all")
def get_revenue(grossrevenue, netrevenue, adminexpenses, depAm, RDexpenses, sellingexpenses, intExpense, IntIncome, grossprofit, beginninginventory, purchases, endinginventory):
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("Select r.GrossSales_Revenue, r.NetSalesRevenue, e.AdministrativeExpenses, e.DepreciationAndAmortization, e.ResearchAndDevelopment, e.SellingExpenses, i.InterestExpense, i.InterestIncome, p.GrossProfit, c.BeginningInventory, c.PlusPurchases, c.LessEnding_Inventory from Revenue r left outer join OperatingExpenses e on r.Year = e.Year left outer join OperatingIncome i on i.Year = r.year left outer join GrossProfit p on p.Year = r.year left outer join COGS c on c.Year = r.year where r.year = 2023")

        for row in cursor.fetchall():
            print(row.grossrevenue, row.netrevenue, row.adminexpenses, row.depAm, row.RDexpenses, row.sellingexpenses, row.intExpense, row.IntIncome, row.grossprofit, row.beginninginventory, row.purchases, row.endinginventory)
            
    return rows


def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn
