"""File API endpoints."""
import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List
from app.schemas.file import UploadResponse, ErrorResponse
from app.services.file_service import file_service
from app.core.config import settings

router = APIRouter()


@router.post('/upload', response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    tool_id: str = Form(...)
):
    """Upload PDF files for processing."""
    # Validate file count
    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f'Too many files. Maximum: {settings.MAX_FILES_PER_UPLOAD}'
        )

    # Generate upload_id first
    upload_id = file_service.generate_upload_id()

    # Validate and save files with order index
    uploaded_files = []
    total_size = 0

    for index, file in enumerate(files):
        file_service.validate_file(file)
        file_id = file_service.generate_file_id()
        # Save file with upload_id and index prefix: {upload_id}_{index:04d}_{file_id}.pdf
        file_info = await file_service.save_uploaded_file_with_index(
            file, file_id, upload_id, index
        )
        uploaded_files.append(file_info)
        total_size += file_info['size']

    # Check total size
    if total_size > settings.MAX_FILE_SIZE * len(files):
        # Clean up uploaded files
        for f in uploaded_files:
            file_service.delete_file_with_prefix(f'{upload_id}_{f["index"]:04d}_{f["file_id"]}')
        raise HTTPException(
            status_code=413,
            detail=f'Total size exceeds limit'
        )

    return UploadResponse(
        success=True,
        data={
            'upload_id': upload_id,
            'files': uploaded_files,
            'total_size': total_size,
            'expires_at': file_service.get_expires_at()
        }
    )


@router.get('/download/{file_id}')
async def download_file(file_id: str):
    """Download processed file.

    Args:
        file_id: File identifier

    Returns:
        File response

    Raises:
        HTTPException: File not found
    """
    from app.core.config import settings

    print(f"[DEBUG] Download request for file_id: {file_id}")

    # Check upload directory
    upload_path = Path(settings.UPLOAD_DIR) / f"{file_id}.pdf"
    if upload_path.exists():
        print(f"[DEBUG] Returning upload file: {upload_path}")
        return FileResponse(
            upload_path,
            media_type='application/pdf',
            filename=upload_path.name
        )

    # Check result directory - prioritize ZIP files
    result_path = Path(settings.RESULT_DIR)

    # First, look for ZIP file
    zip_files = list(result_path.glob(f"{file_id}*.zip"))
    print(f"[DEBUG] Found ZIP files: {zip_files}")

    for file in sorted(zip_files):
        if file.is_file():
            print(f"[DEBUG] Returning ZIP file: {file}")
            return FileResponse(
                file,
                media_type='application/zip',
                filename=file.name
            )

    # Then look for other files
    all_files = list(result_path.glob(f"{file_id}*"))
    print(f"[DEBUG] Found all files: {all_files}")

    for file in sorted(all_files):
        if file.is_file() and file.suffix != '.zip':
            media_type = 'application/pdf'
            if file.suffix == '.txt':
                media_type = 'text/plain'
            elif file.suffix == '.json':
                media_type = 'application/json'

            print(f"[DEBUG] Returning file: {file}, type: {media_type}")
            return FileResponse(
                file,
                media_type=media_type,
                filename=file.name
            )

    print(f"[DEBUG] No file found for {file_id}")
    raise HTTPException(status_code=404, detail='File not found or expired')
