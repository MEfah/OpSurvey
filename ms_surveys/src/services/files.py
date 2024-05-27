from fastapi import UploadFile
import uuid
import aiofiles
import pathlib

class FilesService():
    """Сервис с функциями, необходимыми для работы с файлами
    """
    
    def __init__(self):
        pass
    
    async def save_file(self, file: UploadFile) -> str | None:
        try:
            file_name = uuid.uuid4().hex + '.' + file.filename.split('.')[-1]
            file_path = '/media/surveys/' + file_name
            
            async with aiofiles.open(file_path, 'wb') as file_to:
                content = await file.read()
                await file_to.write(content)
                return file_path
        except:
            return None
        
    def remove_file(self, file_path: str) -> bool:
        try:
            path = pathlib.Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except:
            return False