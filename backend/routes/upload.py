"""
File upload routes for Pilar2
"""

import os
import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import pandas as pd

from config.settings import settings, ENGLISH_TEXTS
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload financial report file (Excel, PDF, CSV)
    Uploading financial report file
    """
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = []
        for extensions in settings.ALLOWED_EXTENSIONS.values():
            allowed_extensions.extend(extensions)
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"{ENGLISH_TEXTS['invalid_file_type']}: {file_extension}"
            )
        
        # Check file size
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=ENGLISH_TEXTS['file_too_large']
            )
        
        # Save file
        file_path = settings.UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded successfully: {file.filename}")
        
        return {
            "message": ENGLISH_TEXTS['upload_success'],
            "filename": file.filename,
            "file_path": str(file_path),
            "file_size": file.size,
            "file_type": file_extension
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ENGLISH_TEXTS['upload_error']
        )

@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    sheet_name: str = Form("Sheet1")
):
    """
    Upload Excel file and extract data
    Uploading Excel file and extracting data
    """
    try:
        # Validate Excel file
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail=f"{ENGLISH_TEXTS['invalid_file_type']}: Excel files only"
            )
        
        # Save file temporarily
        temp_path = settings.UPLOAD_DIR / file.filename
        try:
            # Read the file content first to avoid file pointer issues
            file_content = await file.read()
            logger.info(f"Read {len(file_content)} bytes from uploaded file")
            
            # Save the file
            with open(temp_path, "wb") as buffer:
                buffer.write(file_content)
            logger.info(f"File saved to: {temp_path}")
            logger.info(f"File size: {temp_path.stat().st_size}")
            
            # Verify the file can be read
            try:
                test_df = pd.read_excel(temp_path)
                logger.info(f"File verification successful - {len(test_df)} rows, {len(test_df.columns)} columns")
            except Exception as verify_error:
                logger.error(f"File verification failed: {str(verify_error)}")
                # Check if the file was actually saved
                if temp_path.exists():
                    logger.error(f"Saved file size: {temp_path.stat().st_size}")
                    # Try to read the first few bytes to see what was saved
                    with open(temp_path, 'rb') as f:
                        first_bytes = f.read(20)
                        logger.error(f"First 20 bytes of saved file: {first_bytes.hex()}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Uploaded file appears to be corrupted: {str(verify_error)}"
                )
                
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error saving uploaded file: {str(e)}"
            )
        
        # Read Excel data
        try:
            # First, check what sheets are available in the Excel file
            excel_file = pd.ExcelFile(temp_path)
            available_sheets = excel_file.sheet_names
            
            # If the requested sheet doesn't exist, use the first available sheet
            if sheet_name not in available_sheets:
                if available_sheets:
                    sheet_name = available_sheets[0]
                    logger.info(f"Sheet '{sheet_name}' not found, using first available sheet: '{sheet_name}'")
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Excel file contains no sheets"
                    )
            
            df = pd.read_excel(temp_path, sheet_name=sheet_name)
        except Exception as e:
            logger.error(f"Excel reading error: {str(e)}")
            logger.error(f"File path: {temp_path}")
            logger.error(f"File exists: {temp_path.exists()}")
            if temp_path.exists():
                logger.error(f"File size: {temp_path.stat().st_size}")
            raise HTTPException(
                status_code=400,
                detail=f"Error reading Excel file: {str(e)}"
            )
        
        # Process and save data
        processed_path = settings.PROCESSED_DIR / f"{Path(file.filename).stem}_processed.csv"
        df.to_csv(processed_path, index=False)
        
        logger.info(f"Excel file processed: {file.filename} -> {processed_path}")
        
        # Clean NaN values for JSON serialization
        df_clean = df.fillna('')
        preview_data = df_clean.head().to_dict('records')
        
        return {
            "message": ENGLISH_TEXTS['upload_success'],
            "filename": file.filename,
            "sheet_name": sheet_name,
            "available_sheets": available_sheets,
            "rows": len(df),
            "columns": len(df.columns),
            "processed_path": str(processed_path),
            "preview": preview_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Excel upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ENGLISH_TEXTS['upload_error']
        )

@router.get("/files")
async def list_uploaded_files():
    """
    List all uploaded files
    Listing all uploaded files
    """
    try:
        files = []
        # Get all allowed extensions
        allowed_extensions = []
        for extensions in settings.ALLOWED_EXTENSIONS.values():
            allowed_extensions.extend(extensions)
        
        for file_path in settings.UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                # Skip system files and hidden files
                if file_path.name.startswith('.') or file_path.name in ['.gitkeep', 'Thumbs.db']:
                    continue
                
                # Only include files with supported extensions
                file_extension = Path(file_path.name).suffix.lower()
                if file_extension in allowed_extensions:
                    files.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                        "file_type": file_extension
                    })
        
        return {
            "files": files,
            "total_count": len(files)
        }
        
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error listing uploaded files"
        )

@router.delete("/file/{filename}")
async def delete_file(filename: str):
    """
    Delete uploaded file
    Deleting uploaded file
    """
    try:
        file_path = settings.UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        file_path.unlink()
        logger.info(f"File deleted: {filename}")
        
        return {
            "message": f"File {filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error deleting file"
        )
