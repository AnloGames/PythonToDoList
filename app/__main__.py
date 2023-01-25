import uvicorn
from os import path, curdir
from app import main_app
eng_path = path.abspath(curdir)
print(eng_path)
uvicorn.run(main_app)
