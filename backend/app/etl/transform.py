import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from app.models.student import Student

def process_excel_upload(file_contents: bytes, db: Session):
    # Read Excel file directly from memory bytes
    df = pd.read_excel(BytesIO(file_contents))
    
    # Standardize column names to lower case and strip whitespace
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Core Validation & Cleaning Rules
    # 1. Drop records missing vital identification fields
    df = df.dropna(subset=['roll_no', 'name'])
    
    # 2. Clean up structural spaces and text casings
    df['roll_no'] = df['roll_no'].astype(str).str.strip().str.upper()
    df['name'] = df['name'].astype(str).str.strip()
    df['branch'] = df['branch'].fillna("General").astype(str).str.strip()
    
    # 3. Enforce proper numeric boundaries for CGPA
    df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce').fillna(0.0)
    df['cgpa'] = df['cgpa'].apply(lambda x: min(max(float(x), 0.0), 10.0))
    
    # 4. Handle skills spacing safely
    if 'skills' in df.columns:
        df['skills'] = df['skills'].fillna("").astype(str).str.strip()
    else:
        df['skills'] = ""

    # 5. Prevent duplicate uploads within the sheet itself
    df = df.drop_duplicates(subset=['roll_no'])

    records_added = 0
    
    # Iteratively cross-reference database states to avoid collisions
    for _, row in df.iterrows():
        existing_student = db.query(Student).filter(Student.roll_no == row['roll_no']).first()
        
        if not existing_student:
            new_student = Student(
                roll_no=row['roll_no'],
                name=row['name'],
                branch=row['branch'],
                cgpa=row['cgpa'],
                skills=row['skills']
            )
            db.add(new_student)
            records_added += 1
            
    db.commit()
    return {"status": "success", "records_processed": len(df), "records_inserted": records_added}