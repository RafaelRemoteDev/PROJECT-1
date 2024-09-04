# RAE webscrapping

## Conceptos

### `.gitignore`
Es un archivo de configuración que indica qué archivos y directorios deben ser ignorados por Git.

### `requeriments.txt`

Sirve para:
- Especificar Dependencias: Enumera las bibliotecas y sus versiones exactas que el proyecto necesita para funcionar correctamente.

- Facilitar la Instalación: Permite a otros usuarios instalar todas las dependencias necesarias con un solo comando usando pip: [pip install -r requirements.txt]
- Reproducibilidad: Ayuda a garantizar que el entorno de desarrollo sea consistente y reproducible, ya que todos los colaboradores usan las mismas versiones de las bibliotecas.

## Comandos de Git
- `git add <FICHERO>`para añadir ficheros de interés`en local.
- `git commit -m <MENSAJE>` para añadir los cambios a la rama local.
- `git push` para enviar los cambios al remoto.
- `git rm -rf --cached .idea/` para eliminar los ficheros de Pycharm, luego ponemos en .gitignore ".idea/"


## Enlaces de interés
-[Librería de Pydantic](https://docs.pydantic.dev/latest/concepts/models/): Contiene información sobre cómo construir clases.
