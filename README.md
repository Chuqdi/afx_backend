# Setup

## Install dependencies

dependency manager: poetry https://python-poetry.org/

`poetry install`

## Set VSCode Interpreter

Its helpful to configure your VSCode properly, by setting the python interpreter
in your VSCode for the given project. To do so, run `poetry shell`, copy the
python URI, press CMD+SHIFT+P and paste the URI for the interpreter.

You can test if it worked by creating a new terminal by clicking on "+", you
should see virtual environment activated something like:

`(afx-backend-py3.11) username@machinename afx-backend $`

instead of

`username@machinename afx-backend $`

## Test run

Use VSCode Debugger at all times during the development for properly working
with the template and keep track of bugs not wasting time rerunning the backend
when something goes wrong.

Go to Debugger and choose `Start` in the dropdown.

After that, you can get access to the API docs on

`http://0.0.0.0:8000/docs`

On top right, you should authorize yourself.


## Automated Tests

`pytest`

# Main Stack

- ODM: https://beanie-odm.dev/
- FastAPI: https://fastapi.tiangolo.com/

# Check Coverage

`coverage report -m`
