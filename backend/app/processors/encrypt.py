"""PDF encryption/decryption processor."""

from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("encrypt_decrypt")
class EncryptDecryptProcessor(BaseProcessor):
    """Processor for encrypting and decrypting PDF files."""

    async def process(
        self, job_id: str, files: list[Path], options: Dict[str, Any]
    ) -> str:
        """Process PDF encryption or decryption.

        Args:
            job_id: Job identifier
            files: List of PDF file paths (should be single file)
            options: Processing options (operation, password, new_password, algorithm)

        Returns:
            Output file ID

        Raises:
            Exception: Processing failed
        """
        # Update status
        job_service.update_job(job_id, status="processing", started_at=datetime.now())

        if not files:
            raise ValueError("No files provided")

        file_path = files[0]
        operation = options.get("operation", "encrypt")

        try:
            if operation == "encrypt":
                return await self._encrypt_pdf(job_id, file_path, options)
            elif operation == "decrypt":
                return await self._decrypt_pdf(job_id, file_path, options)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except Exception as e:
            job_service.fail_job(
                job_id, {"code": "ERR_ENCRYPT_DECRYPT_FAILED", "message": str(e)}
            )
            raise

    async def _encrypt_pdf(
        self, job_id: str, file_path: Path, options: Dict[str, Any]
    ) -> str:
        """Encrypt PDF with password.

        Args:
            job_id: Job identifier
            file_path: Input PDF file path
            options: Encryption options

        Returns:
            Output file ID
        """
        password = options.get("password", "")
        algorithm = options.get("algorithm", "AES-256")
        allow_printing = options.get("allow_printing", True)
        allow_copying = options.get("allow_copying", False)
        allow_modifying = options.get("allow_modifying", False)

        if not password:
            raise ValueError("Password is required for encryption")

        # Map algorithm to PyMuPDF encryption method
        encryption_map = {
            "AES-256": fitz.PDF_ENCRYPT_AES_256,
            "AES-128": fitz.PDF_ENCRYPT_AES_128,
            "RC4-128": fitz.PDF_ENCRYPT_RC4_128,
            "RC4-40": fitz.PDF_ENCRYPT_RC4_40,
        }
        encryption_method = encryption_map.get(algorithm, fitz.PDF_ENCRYPT_AES_256)

        # Build permissions - these are the operations that ARE ALLOWED
        # Start with minimal permissions (only accessibility for screen readers)
        permissions = fitz.PDF_PERM_ACCESSIBILITY  # Always allow accessibility

        if allow_printing:
            permissions |= fitz.PDF_PERM_PRINT | fitz.PDF_PERM_PRINT_HQ

        if allow_copying:
            permissions |= fitz.PDF_PERM_COPY | fitz.PDF_PERM_ANNOTATE

        if allow_modifying:
            permissions |= (
                fitz.PDF_PERM_MODIFY | fitz.PDF_PERM_ASSEMBLE | fitz.PDF_PERM_FORM
            )

        # Validate PDF (check if already encrypted)
        try:
            doc = fitz.open(file_path)
            if doc.is_encrypted:
                doc.close()
                raise ValueError("PDF is already encrypted. Please decrypt it first.")
            page_count = len(doc)
            doc.close()
        except Exception as e:
            if "already encrypted" in str(e):
                raise
            raise ValueError(f"Invalid PDF file: {e}")

        # Generate output filename
        original_name = file_path.stem
        output_filename = f"{original_name}_encrypted.pdf"
        output_path = self.get_output_path(job_id, output_filename)

        self.update_progress(job_id, 30, "Encrypting PDF...")

        # Reopen and encrypt
        doc = fitz.open(file_path)

        # Save with encryption
        doc.save(
            output_path,
            encryption=encryption_method,
            owner_pw=password,
            user_pw=password,
            permissions=permissions,
        )
        doc.close()

        self.update_progress(job_id, 80, "Finalizing...")

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(
            job_id,
            {
                "output_file_id": job_id,
                "filename": output_filename,
                "size": file_size,
                "pages": page_count,
                "download_url": f"/api/v1/files/download/{job_id}",
                "expires_at": (
                    datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)
                ).isoformat(),
            },
        )

        return job_id

    async def _decrypt_pdf(
        self, job_id: str, file_path: Path, options: Dict[str, Any]
    ) -> str:
        """Decrypt PDF with password.

        Args:
            job_id: Job identifier
            file_path: Input PDF file path
            options: Decryption options

        Returns:
            Output file ID
        """
        password = options.get("password", "")

        if not password:
            raise ValueError("Password is required for decryption")

        # Try to open with password
        try:
            doc = fitz.open(file_path)

            if not doc.is_encrypted:
                doc.close()
                raise ValueError("PDF is not encrypted")

            # Try to authenticate
            auth_result = doc.authenticate(password)
            if not auth_result:
                doc.close()
                raise ValueError("Incorrect password")

            page_count = len(doc)
            doc.close()
        except ValueError as e:
            raise
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")

        # Generate output filename
        original_name = file_path.stem
        # Remove "_encrypted" suffix if present
        if original_name.endswith("_encrypted"):
            original_name = original_name[:-10]
        output_filename = f"{original_name}_decrypted.pdf"
        output_path = self.get_output_path(job_id, output_filename)

        self.update_progress(job_id, 30, "Decrypting PDF...")

        # Reopen, decrypt and save without encryption
        doc = fitz.open(file_path)
        doc.authenticate(password)

        # Save without encryption
        doc.save(output_path)
        doc.close()

        self.update_progress(job_id, 80, "Finalizing...")

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(
            job_id,
            {
                "output_file_id": job_id,
                "filename": output_filename,
                "size": file_size,
                "pages": page_count,
                "download_url": f"/api/v1/files/download/{job_id}",
                "expires_at": (
                    datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)
                ).isoformat(),
            },
        )

        return job_id
