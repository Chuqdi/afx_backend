from fastapi import HTTPException, UploadFile, status
from typing import List

class AllowedExtensions:
    def __init__(self, allowed_extensions: List[str], max_size: int = 5 * 1024 * 1024):  # Default max size is 5 MB
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size

    def __call__(self, file: UploadFile):
        # Check file extension
        if not file.content_type.startswith("image/") or not file.filename.split(".")[-1] in self.allowed_extensions: # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image")

        # Check file size
        if file.file.__sizeof__() > self.max_size:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds the allowed limit")

        return file
