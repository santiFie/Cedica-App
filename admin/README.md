## Aplicación Web de CEDICA
### Contexto
El Centro de Equitación para Personas con Discapacidad y Carenciadas (CEDICA) es una Asociación Civil sin Fines de Lucro fundada en 1994 en La Plata, Argentina. CEDICA busca igualar oportunidades y mejorar la calidad de vida de las personas con discapacidad a través de Terapias y Actividades Asistidas con Caballos (TACAs). El equipo está compuesto por profesionales ecuestres, terapistas, psicólogos, educadores y voluntarios.

### Objetivo
El objetivo de esta aplicación es digitalizar y gestionar la información de los diferentes procesos de trabajo de la institución. Los usuarios directos son los integrantes del equipo de CEDICA, quienes podrán acceder a los registros históricos de Jinetes y Amazonas (J&A), profesionales, caballos, y generar reportes estadísticos.

### Funcionalidades
La aplicación permite:

- Mantener un registro histórico de los legajos de los J&A, incluyendo documentos necesarios.
- Registrar y gestionar la información de los profesionales del equipo.
- Registrar la información de los caballos utilizados en las terapias.
- Obtener reportes estadísticos sobre los datos almacenados.


### Utilización
Para poder utilizar la aplicación debe ingresar al siguiente [link](https://admin-grupo43.proyecto2024.linti.unlp.edu.ar/)

En caso de querer ejecutar la aplicación localmente debe seguir estos pasos:

#### 1. Instalación de dependencias iniciales

Asegúrate de tener instalados los siguientes programas:

Python (>=3.12) [Python](https://www.python.org/downloads/)
Node.js

#### 2. Clonar el repositorio
\`\`\`bash
git clone https://gitlab.catedras.linti.unlp.edu.ar/proyecto2024/proyectos/grupo43/code.git
cd proyecto
\`\`\`

#### 3. Configurar el entorno virtual con Poetry
Si no tienes Poetry instalado, instálalo con aquí esta la [Guía de instalación](https://github.com/python-poetry/install.python-poetry.org)

Luego, instala las dependencias del proyecto ejecutando:
\`\`\`bash
poetry install
\`\`\`
Opcional: Si prefieres trabajar dentro de un entorno virtual manejado por Poetry, actívalo con:
\`\`\`bash
poetry shell
\`\`\`

#### 4. Configuración de las variables de entonro
Como no se incluyen variables de entorno, puedes definirlas manualmente. Asegurate de que coincidan con la configuración del archivo docker-compose.yml

#### 5. Inicialización del contenedor docker.
Levanta los servicios de Docker necesarios para la aplicación:
\`\`\`bash
docker-compose up -d
\`\`\`

#### 6. Inicialización de la base de datos
Para configurar la base de datos, ejecuta el siguiente comando desde el directorio del proyecto:
\`\`\`bash
flask reset-db
\`\`\`

#### 7. Compilar los estilos con TailwindCSS
Configura nodeenv para crear un entorno aislado de Node.js:
\`\`\`bash
nodeenv env_node
source env_node/bin/activate
\`\`\`

Luego, ejecuta:

\`\`\`bash
npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
\`\`\`
Esto compilará los estilos de TailwindCSS y los mantendrá actualizados en tiempo real

#### 8. Ejecutar la aplicación
Para iniciar el servidor local de Flask, usa:
\`\`\`bash
flask run
\`\`\`
El servidor estará disponible en http://127.0.0.1:5000.

### Dependencias

Este proyecto utiliza las siguientes dependencias, gestionadas a través de [Poetry](https://python-poetry.org/):

- **email-validator 2.2.0**: Validación de sintaxis y entregabilidad de direcciones de correo electrónico.
- **Flask 3.0.3**: Framework para la creación de aplicaciones web complejas.
- **flask-bcrypt 1.0.1**: Hashing con bcrypt para Flask.
- **flask-session 0.8.0**: Soporte para sesiones del lado del servidor en Flask.
- **flask-sqlalchemy 3.1.1**: Soporte para SQLAlchemy en aplicaciones Flask.
- **minio 7.2.9**: SDK de Python para almacenamiento en la nube compatible con S3.
- **nodeenv 1.9.1**: Entorno virtual para Node.js.
- **psycopg2-binary 2.9.9**: Adaptador de base de datos Python-PostgreSQL.
- **pytest 8.3.2**: Framework de pruebas en Python.
- **tailwindcss 0.0.1**: Para utilizar Tailwind CSS.
- **wtforms 3.1.2**: Validación y renderización de formularios para desarrollo web en Python.

### Licencia
Esta aplicación está licenciada bajo la Licencia MIT, permitiendo su libre uso y modificación.