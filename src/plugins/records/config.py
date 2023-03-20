from pydantic import BaseModel, Extra
from typing import List, Dict


class Config(BaseModel, extra=Extra.ignore):
    ocr_url : str = 'http://localhost:8089/api/tr-run/'
    record_path: str = ''
    inverted_index_path: str = ''
    tmp_dir: str = ''
    quote_superuser: Dict[str, List[str]] = {}






