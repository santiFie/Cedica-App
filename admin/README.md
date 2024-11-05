## Aplicación Web de CEDICA
### Contexto
El Centro de Equitación para Personas con Discapacidad y Carenciadas (CEDICA) es una Asociación Civil sin Fines de Lucro fundada en 1994 en La Plata, Argentina. CEDICA busca igualar oportunidades y mejorar la calidad de vida de las personas con discapacidad a través de Terapias y Actividades Asistidas con Caballos (TACAs). El equipo está compuesto por profesionales ecuestres, terapistas, psicólogos, educadores y voluntarios.aaa

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