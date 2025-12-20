from typing import Tuple, Optional

from flask import jsonify

from src.application.api.errors.error_code import ErrorCode


class APIError:

    def __init__(self, error_code: ErrorCode, title: str, details: Optional[str], http_status: int):
        self.error_code = error_code
        self.title = title
        self.details = details
        self.http_status = http_status

    def to_api(self) -> Tuple[jsonify, int]:
        return {
            "code": self.error_code.value,
            "title": self.title,
            "details": self.details
        }, self.http_status
