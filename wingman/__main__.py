import os

import dotenv

dotenv.load_dotenv()
print(os.getenv("GITHUB_PERSONAL_TOKEN"))

from wingman.todo import parse as parse
