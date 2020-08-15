import os
import base64
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def _get_project_root_directory():
    dirname, _ = os.path.split(os.path.abspath("__file__"))
    root_dir = os.path.dirname(dirname)
    return root_dir


def _read_key():
    root_dir = _get_project_root_directory()
    password_file = os.path.join(root_dir, "password")
    if not os.path.exists(password_file):
        raise FileNotFoundError("password file not found in the project's root directory")

    with open(password_file, "r") as f:
        password = f.read()
        if len(password) <= 0:
            raise ValueError("password file cannot be empty")
        return password


def _get_key(password):
    password = password.encode()  # convert the string password to bytes
    salt = b'\x8f\x7fDN\x1d*\xda\x06Gff-\xf2\xf8\x13\x00'  # generate a salt using os.random(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def _encrypt_file(password, filename):
    if not os.path.exists(filename):
        _, _filename = os.path.split(filename + ".enc")
        if _filename.endswith(".enc"):
            print("{0} is already encrypted".format(_filename))
            return
        raise FileNotFoundError("{0} not exists".format(filename))

    _dirname, _filename = os.path.split(filename)
    _filename = _filename + '.enc'
    if os.path.exists(os.path.join(_dirname, _filename)):
        print("an encrypted file with the same name '{0}', is already present".format(_filename))
        return

    key = _get_key(password=password)
    with open(filename, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data=data)

    with open("{0}.enc".format(filename), 'wb') as file:
        file.write(encrypted)

    if os.path.exists(filename):
        os.remove(filename)


def _decrypt_file(password, filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("{0} not exists".format(filename))

    key = _get_key(password=password)
    with open(filename, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(token=data)

    lines = decrypted.decode().split("\n")
    app_keys = {}
    for line in lines:
        line_key = line.strip().split("=")[0].strip()
        line_value = line.strip().split("=")[1].strip()
        app_keys[line_key] = line_value
    return app_keys


def secure_secrets(project_name):
    password = _read_key()
    root_dir = _get_project_root_directory()
    project_dir = os.path.join(root_dir, project_name)
    if not os.path.exists(project_dir):
        raise FileNotFoundError("project do not exist")

    secrets_path = os.path.join(project_dir, "secrets")
    secrets_enc_path = ""
    if not os.path.exists(secrets_path):
        secrets_enc_path = os.path.join(project_dir, "secrets.enc")
        if os.path.exists(secrets_enc_path):
            secrets_path = secrets_enc_path
        else:
            raise FileNotFoundError("secrets file not found in the project")

    if secrets_path != secrets_enc_path:
        _encrypt_file(password=password, filename=secrets_path)
        # secrets_path = '{}.enc'.format(secrets_path)
        logging.info("secured the secrets")
    else:
        logging.info("secrets is already secured")


def read_secrets(project_name):
    password = _read_key()
    root_dir = _get_project_root_directory()
    project_dir = os.path.join(root_dir, project_name)
    if not os.path.exists(project_dir):
        raise FileNotFoundError("project do not exist")

    secrets_enc_path = os.path.join(project_dir, "secrets.enc")
    if not os.path.exists(secrets_enc_path):
        secrets_path = os.path.join(project_dir, "secrets")
        if os.path.exists(secrets_path):
            raise RuntimeError("secrets found but this must be secured first")
        else:
            raise RuntimeError("no secrets found")

    return _decrypt_file(password=password, filename=secrets_enc_path)


if __name__ == "__main__":
    project = "mailing-client"
    secure_secrets(project)
    keys = read_secrets(project)
    print(keys)
