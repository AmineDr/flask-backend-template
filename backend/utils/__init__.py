from hashlib import sha512, md5
from random import choices
from string import ascii_letters
from PIL import Image
import os


class PrivilegeService:
    def __init__(self, privileges):
        self.privileges = privileges
        if not privileges:
            self.privileges = []

    def has_access(self, privilege_name: str, privilege_level: int) -> bool:
        for privilege in self.privileges:
            if privilege.level < privilege_level:
                continue
            if privilege.name == 'ALL' or privilege.name == privilege_name:
                return True
        return False

    @staticmethod
    def has_admin_header(headers: dict) -> bool:
        """
         SETUP FOR CUSTOM HEADER FOR ADMINS
         """
        return headers.get('X-CUSTOM_HEADER') == "CUSTOM_HEADER_VALUE"


def check_privilege(**kwargs):
    perm = kwargs.get('perm')
    level = kwargs.get('level')

    def decorator(func):
        def wrapper(*args):
            root_user = args[0].root_user
            if root_user is not None:
                if PrivilegeService(root_user.privileges).has_access(perm, level):
                    return func(*args)
                return {"status": "forbidden"}, 403
            return {"status": "unauthorized"}, 401
        return wrapper
    return decorator


def gen_id(seed='', length=40, random_scale=20):
    server_short = os.environ.get("SERVER_SHORT_NAME")
    if server_short is None:
        server_short = "C45"
    if seed:
        return f'{server_short}-'+md5(seed.encode()).hexdigest().upper()
    if isinstance(length, int) and isinstance(random_scale, int):
        return sha512(''.join(choices(ascii_letters, k=20)).encode()).hexdigest()[:length]
    else:
        raise TypeError("Integer expected in function gen_id.")


def compress_image(input_image_path, output_image_path, ext, quality=80):
    original_image = Image.open(input_image_path)
    compression_format = "JPEG" if ext == "jpg" or ext == "jpeg" else "PNG"
    original_image.save(output_image_path, compression_format, quality=quality, optimize=True)

