from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Our own files: Pydantic schemas and the DB connection helper
from model import OpportunityCreate, OpportunityUpdate
from database import get_connection

# Create the FastAPI application instance.
# Every route (@app.get, @app.post, etc.) attaches itself to this object.
app = FastAPI(title="Research Opportunity Portal API")

# CORS = Cross-Origin Resource Sharing.
# Browsers block JS on one origin (e.g. your frontend HTML file opened locally)
# from calling an API on a different origin (e.g. localhost:8000) unless the
# server explicitly allows it. This middleware says "allow everyone, every
# method, every header" — fine for a university assignment, not for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# By default, when Pydantic validation fails (e.g. missing required field,
# wrong type), FastAPI returns HTTP 422. The assignment specifically asks
# for 400 Bad Request, so we override that default behavior here.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


# ---------- 1. CREATE ----------
# POST /api/opportunities
# "opp: OpportunityCreate" tells FastAPI to parse the incoming JSON body
# and validate it against our Pydantic model BEFORE this function even runs.
# If validation fails, the exception handler above kicks in automatically.
@app.post("/api/opportunities", status_code=201)
def create_opportunity(opp: OpportunityCreate):
    conn = get_connection()       # open a connection to MySQL
    cursor = conn.cursor()        # cursor = object used to execute SQL and fetch results

    # %s placeholders are parameter markers. The driver safely inserts the
    # actual values below, preventing SQL injection. Never use f-strings
    # to build SQL with user input.
    query = """INSERT INTO opportunities 
        (title, description, research_area, faculty_name, department, 
         required_skills, available_positions, application_deadline, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (opp.title, opp.description, opp.research_area, opp.faculty_name,
              opp.department, opp.required_skills, opp.available_positions,
              opp.application_deadline, opp.status.value)  # .value converts enum -> plain string

    try:
        cursor.execute(query, values)   # run the INSERT
        conn.commit()                   # commit = actually save the change to the DB
        new_id = cursor.lastrowid       # MySQL auto-generated ID of the row we just inserted
        return {"id": new_id, "message": "Opportunity created successfully"}
    except Exception as e:
        # Anything unexpected (DB down, constraint violation, etc.) -> 500
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # finally always runs, whether we succeeded or hit the except block,
        # so we never leak an open DB connection.
        cursor.close()
        conn.close()


# ---------- 2. READ ALL ----------
# GET /api/opportunities
@app.get("/api/opportunities")
def get_all_opportunities():
    conn = get_connection()
    # dictionary=True makes each row come back as {"column_name": value, ...}
    # instead of a plain tuple, so FastAPI can convert it to JSON cleanly.
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opportunities")
    result = cursor.fetchall()   # fetchall() = get every row from the query
    cursor.close()
    conn.close()
    return result   # FastAPI auto-converts this list of dicts into a JSON array


# ---------- 3. READ ONE ----------
# GET /api/opportunities/{opp_id}
# "{opp_id}" in the path becomes a function parameter. FastAPI also
# validates it's an int automatically (e.g. /api/opportunities/abc -> 422/400).
@app.get("/api/opportunities/{opp_id}")
def get_opportunity(opp_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opportunities WHERE id = %s", (opp_id,))
    result = cursor.fetchone()   # fetchone() = get a single row (or None)
    cursor.close()
    conn.close()
    if not result:
        # No row found with that ID -> this is the 404 case the assignment requires
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return result


# ---------- 4. UPDATE ----------
# PUT /api/opportunities/{opp_id}
@app.put("/api/opportunities/{opp_id}")
def update_opportunity(opp_id: int, opp: OpportunityUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # First check the row actually exists before trying to update it
    cursor.execute("SELECT * FROM opportunities WHERE id = %s", (opp_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # exclude_unset=True means: only include fields the client actually sent
    # in the JSON body. This lets someone update just "status" without
    # overwriting every other field with None.
    update_fields = {k: v for k, v in opp.dict(exclude_unset=True).items()}

    if not update_fields:
        # Client sent an empty update (e.g. {}) -> that's a bad request
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # status comes in as an Enum object (StatusEnum.open); MySQL needs the
    # plain string "Open", so we unwrap it here if present.
    if "status" in update_fields:
        update_fields["status"] = update_fields["status"].value

    # Dynamically build "column1 = %s, column2 = %s, ..." based on whichever
    # fields were actually sent.
    set_clause = ", ".join([f"{k} = %s" for k in update_fields])
    values = list(update_fields.values()) + [opp_id]   # +[opp_id] for the WHERE clause

    try:
        cursor.execute(f"UPDATE opportunities SET {set_clause} WHERE id = %s", values)
        conn.commit()
        return {"message": "Opportunity updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ---------- 5. DELETE ----------
# DELETE /api/opportunities/{opp_id}
@app.delete("/api/opportunities/{opp_id}")
def delete_opportunity(opp_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Check existence first so we can return a proper 404 instead of
    # silently "succeeding" on a delete that did nothing.
    cursor.execute("SELECT id FROM opportunities WHERE id = %s", (opp_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Opportunity not found")

    cursor.execute("DELETE FROM opportunities WHERE id = %s", (opp_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Opportunity deleted successfully"}