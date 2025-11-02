'''
  db helper
'''
from sqlite3 import connect,Row
from os import system

database:str ="db/school.db"

def getprocess(sql,vals:list=[])->list:
    conn:any = connect(database)
    conn.row_factory = Row
    cursor:any = conn.cursor()
    cursor.execute(sql,vals)
    data:list = cursor.fetchall()
    cursor.close()
    conn.close()
    return data 
        
def postprocess(sql:str,vals:list=[])->bool:
    try:
        conn:any = connect(database)
        cursor:any = conn.cursor()
        cursor.execute(sql,vals)
        conn.commit()
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()
    return True if cursor.rowcount>0 else False

#crud
def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql,[])
    
def getrecord(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append(f"`{key}`=?")
    fields:str = " AND ".join(flds)
    sql:str = f"SELECT * FROM `{table}` WHERE {fields}"
    return getprocess(sql,vals)
    
def addrecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    dats:list = ['?']*len(keys)
    datstring:str = ",".join (dats)
    fields:str = "`,`".join(keys)
    sql:str = f"INSERT INTO `{table}` (`{fields}`) VALUES ({datstring})"
    return postprocess(sql,vals)
    
def deleterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append(f"`{key}`=?")
    fields:str = " AND ".join(flds)
    sql:str = f"DELETE FROM `{table}` WHERE {fields}"
    return postprocess(sql,vals)
    
# def updaterecord(table:str,**kwargs)->bool:
#     keys:list = list(kwargs.keys())
#     vals:list = list(kwargs.values())
#     newvals:list = []
#     flds:list = []
#     for index in range(1,len(keys)):
#         flds.append(f"`{keys[index]}`=?")
#         newvals.append({vals[index]})
#     fields:str = ",".join(flds)   
#     sql = f"UPDATE `{table}` SET {fields} WHERE `{keys[0]}`=?"
#     newvals.append(vals[0])
#     return postprocess(sql,newvals)

def updaterecord(table: str, where: dict, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    sets = ",".join([f"`{k}`=?" for k in keys])

    w_keys = list(where.keys())
    w_vals = list(where.values())
    w_clause = " AND ".join([f"`{k}`=?" for k in w_keys])

    sql = f"UPDATE `{table}` SET {sets} WHERE {w_clause}"
    return postprocess(sql, vals + w_vals)