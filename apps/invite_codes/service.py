import random
import string

from apps.invite_codes.repository import InviteCodeRepository
from apps.invite_codes.serializers import InviteCodeSerializer


class InviteCodeService:
    @staticmethod
    def create():
        length = 6
        while True:
            num_letters = random.randint(1, 5)
            num_digits = length - num_letters
            letters = random.choices(
                string.ascii_letters,
                k=num_letters
            )
            digits = random.choices(
                string.digits,
                k=num_digits
            )
            code_list = letters + digits
            random.shuffle(code_list)
            code = ''.join(code_list)
            invite_code = InviteCodeSerializer(
                data={'code': code}
            )
            code = InviteCodeRepository().get(
                invite_code
            )
            if not code:
                return InviteCodeRepository().create(
                    invite_code
                )
