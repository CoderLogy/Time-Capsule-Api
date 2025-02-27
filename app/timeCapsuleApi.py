from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import uuid
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing all origins for testing purposes (you can specify specific domains later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; for production, use specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome To TimeCapsule"}

# The code snippet `app = FastAPI()` creates a FastAPI application instance, which is the main entry
# point for defining API routes and handling HTTP requests. This instance is used to define the API
# endpoints and their corresponding functions.
app = FastAPI()
DATA_FILE = "Capsules.json"


# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# The `Capsule` class defines a data structure with attributes for a message and an open date.
class Capsule(BaseModel):
    message: str
    open_date: str

def load_capsules():
    """
    The function `load_capsules` reads and returns the contents of a JSON file named `DATA_FILE`.
    :return: The function `load_capsules()` is returning the data loaded from the file specified by the
    `DATA_FILE` constant using the `json.load()` method.
    """
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# The `save_capsules(data)` function is responsible for saving the updated data back to the JSON file
# specified by the `DATA_FILE` constant.
def save_capsules(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

capsules = load_capsules()

@app.post('/Capsule/')
def store_capsule(capsule: Capsule):
    """
    The function `store_capsule` stores a capsule object in a list and saves it to a file, returning the
    capsule ID.
    
    :param capsule: Capsule object containing information such as message and open date
    :type capsule: Capsule
    :return: The function `store_capsule` is returning a dictionary with two key-value pairs:
    1. "message": "Capsule Stored!"
    2. "id": capsule_id
    """
    capsule_id: str = str(uuid.uuid4())
    new_capsule = {
        "capsule_id": capsule_id,
        "message": capsule.message,
        "open_date": capsule.open_date
    }
    capsules.append(new_capsule)
    save_capsules(capsules)
    return {"message": "Capsule Stored!","id": capsule_id}
@app.get('/Capsule/Search')
def get_capsule(capsule_id:str):
    """
    The function `get_capsule` retrieves a capsule's message based on its ID, checking if it can be
    opened based on the open date.
    
    :param capsule_id: It looks like you are trying to define a function `get_capsule` that takes a
    `capsule_id` as a parameter. The function iterates through a list of capsules and checks if the
    `capsule_id` matches the id of any capsule in the list. If a match is found
    :type capsule_id: str
    :return: If the capsule with the given `capsule_id` exists in the `capsules` list and the current
    date is greater than or equal to the `open_date` of the capsule, then the message inside that
    capsule is returned in a dictionary format like {"message": capsule["message"]}.
    """
    for capsule in capsules:
        if capsule["capsule_id"] == capsule_id:
            if datetime.strptime(capsule["open_date"],"%Y-%m-%d") <= datetime.today():
                return {"message":capsule["message"]}
            else:
                return {"message": f"Date mismatched, can't open it before {capsule['open_date']}"}
    raise HTTPException(status_code=404, detail="Capsule Not Found")
@app.get('/Capsule/List')
def list_capsule():
    """
    This Python function creates a list of available capsules based on their open dates.
    :return: If the current date is before or equal to the open date of any capsule in the `capsules`
    list, the function will return a dictionary containing a key "list_of_all_availiable_capsule" with a
    list of dictionaries, each representing an available capsule with its id and open date. If there are
    no available capsules (i.e., all capsules have open dates in the past), the function
    """
    list_of_all_availiable_capsule = []
    for capsule in capsules:
        if datetime.strptime(capsule["open_date"],"%Y-%m-%d"): #>= datetime.today():
            list_of_all_availiable_capsule.append({"id": capsule["capsule_id"], "open_date": capsule["open_date"]})
        else:
            return {"message": "No Capsule Found!"}
    return {"list_of_all_availiable_capsule": list_of_all_availiable_capsule}
@app.delete('/Capsule/Delete')
def delete_capsule(capsule_id:str):
    """
    The function `delete_capsule` takes a capsule ID as input and deletes the corresponding capsule from
    a list of capsules, raising a 404 error if the capsule is not found.
    
    :param capsule_id: The `delete_capsule` function takes a `capsule_id` parameter as input, which is a
    string representing the ID of the capsule that needs to be deleted. The function then attempts to
    find and delete the capsule with the specified ID from a list of capsules. If the capsule is
    successfully deleted
    :type capsule_id: str
    :return: a dictionary with a key "message" and the value "Capsule Deleted Successfully!"
    """
    new_capsule = [capsule for capsule in capsules if capsule["capsule_id"] != new_capsule]
    if len(new_capsule) == len(capsules):
        raise HTTPException(status_code=404, detail="Capsule Not Found to delete")
    else:
        save_capsules(new_capsule)
        return{"message": "Capsule Deleted Successfully!"}
