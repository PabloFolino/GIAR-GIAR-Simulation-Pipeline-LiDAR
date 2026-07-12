1- Crear y activar un entorno virtual
    py -3.11 -m venv .venv
    .\.venv\Scripts\activate
    python -m pip install --upgrade pip

2- Instalar las librerias:
    pip install rhino3dm
    pip install numpy 
    pip install scipy
    pip install pyyaml
    pip install lxml
    pip install openpyxl
    pip freeze > requirements.txt

3- Para salir del entorno virtual: deactivate