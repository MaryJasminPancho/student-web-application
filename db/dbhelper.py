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
    conn:any = connect(database)
    cursor:any = conn.cursor()
    cursor.execute(sql,vals)
    conn.commit()
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
    qmark:list = ['?']*len(vals)
    dta:str = ",".join(qmark)
    fields:str ="`,`".join(keys)
    sql:str = f"INSERT INTO `{table}`(`{fields}`) VALUES({dta})"
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
    
def updaterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    newvals:list = []
    flds:list = []
    for index in range(1,len(vals)):
        flds.append(f"`{keys[index]}`=?")
        newvals.append(f"{vals[index]}")
    fields:str = ",".join(flds)   
    sql:str = f"UPDATE `{table}` SET {fields} WHERE `{keys[0]}`='{vals[0]}'"
    return postprocess(sql,newvals)


def main()->None:
    students:list = getall('students')
    for student in students:
        print(f"{student ['idno']} {student ['lastname']} {student ['firstname']}")

if __name__ == "__main__":
    main()