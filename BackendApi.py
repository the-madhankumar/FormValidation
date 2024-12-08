from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()


# Uncomment to create the table the first time
# create_table_query = """
# CREATE TABLE IF NOT EXISTS Employee (
#     Name TEXT NOT NULL,
#     EmployeeID TEXT PRIMARY KEY,
#     Email TEXT NOT NULL,
#     PhoneNumber TEXT NOT NULL,
#     Department TEXT NOT NULL,
#     DateOfJoining TEXT NOT NULL,
#     Role TEXT NOT NULL
# );
# """
# cur.execute(create_table_query)

# Pydantic model for request validation
class Employee(BaseModel):
    Name: str
    EmployeeID: str
    Email: str
    PhoneNumber: str
    Department: str
    DateOfJoining: str
    Role: str

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("Forms.db", check_same_thread=False)
    return conn

@app.post('/insert')
def insert_in(employee: Employee):
    print(f"Received employee data: {employee}")
    
    employee_data = (employee.Name, employee.EmployeeID, employee.Email, 
                     employee.PhoneNumber, employee.Department, 
                     employee.DateOfJoining, employee.Role)
    
    # Insert query
    insert_query = """
    INSERT INTO Employee (Name, EmployeeID, Email, PhoneNumber, Department, DateOfJoining, Role)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    try:
        # Use a new connection for each request
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(insert_query, employee_data)
        conn.commit()
        
        # Print success message to terminal
        print("Data inserted successfully into the database.")
        
        return {"message": "Data inserted successfully"}
    except Exception as e:
        print(f"Error during insert: {str(e)}")
        return {"error": "EmployeeId already Exist", "details": str(e)}
    finally:
        # Close the database connection
        conn.close()

@app.get('/')
def get_all():
    select_query = "SELECT * FROM Employee"
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(select_query)
        
        # Fetch all data
        data = cur.fetchall()
        
        
        return data
    except Exception as e:
        # Print error message to terminal
        print(f"Error during fetching data: {str(e)}")
        return {"error": "Internal server error", "details": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
