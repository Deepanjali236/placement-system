from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import student, upload, interview  # Added interview here

# Re-evaluates database tables, compiling the new Interviews entity
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Placement System API")

app.include_router(student.router)
app.include_router(upload.router)
app.include_router(interview.router)  # Registered here!
from fastapi.responses import RedirectResponse

@app.get("/")
def home():
    # This automatically sends anyone who visits the main link straight to the docs!
    return RedirectResponse(url="/docs")