# Python Networking

Copy the `password.template` in the root directory of the project as `password`. This `password` will contain your key for encryption and decryption.
Provide a very strong key in here. The directory looks as shown below

The structure of a project with `secrets` is shown below
```
.
├── commons
│   ├── __init__.py
│   └── secure.py
├── project-directory
│   ├── __init__.py
│   ├── main.py
│   └── secrets
├── password
└── README.md
```

> Caution: Never upload this `password` file

Each project may contain some sensitive information's. It is not a good idea to expose them, hence encrypt it based on your password.

The secrets needs to be first stored in a file named `secrets` in the project directory.
A secret will be a key-value pair based as shown below
```python
key1=value1
key2=value2
```
Copy the `secrets.template` in the project directory as `secrets` and add your secrets in there. Run the below piece of code to encrypt the `secrets`.
```python
from commons import secure, common
_, project_name = common.get_project_dir_name()
secure.secure_secrets(project_name)
```