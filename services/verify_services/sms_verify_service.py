import time
import random
import string

from apps.authentication.serializers import VerifyCodeSerializer
from utils.verify_service import AbstractVerifyService

class SmsVerifyService(AbstractVerifyService):
    def send_code(self, code: str) -> None:
        time.sleep(1)

    def create_code(self) -> VerifyCodeSerializer:
        auth_code = ''.join(
            random.choices(string.digits, k=4)
        )
        self.send_code(auth_code)
        return VerifyCodeSerializer(
            data={'code': auth_code}
        )
