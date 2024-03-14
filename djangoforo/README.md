# Documentación de API

Bienvenido a la documentación de la API de ChatWave. Acá encontrarás información sobre los endpoints disponibles en la API y cómo utilizarlos.

## Tabla de Contenidos

- [Documentación de API](#documentación-de-api)
  - [Tabla de Contenidos](#tabla-de-contenidos)
- [Endpoints](#endpoints)
  - [Usuario](#usuario)
    - [Registro de Usuario](#registro-de-usuario)
    - [Inicio de Sesión](#inicio-de-sesión)
    - [Información del usuario con sesión iniciada](#información-del-usuario-con-sesión-iniciada)
    - [Editar detalles del usuario](#editar-detalles-del-usuario)
    - [Ver el perfil de un usuario](#ver-el-perfil-de-un-usuario)
    - [Cerrar Sesión](#cerrar-sesión)
  - [Salas](#salas)

    
# Endpoints 

## Usuario

### Registro de Usuario

- **URL**: `/api/authentication/register/`
- **Método HTTP**: `POST`
- **Descripción**: Este endpoint permite a los usuarios registrarse en la plataforma.
- **Parámetros de Entrada**:
  - `first_name` (string): Nombre del usuario.
  - `last_name` (string): Apellido del usuario.
  - `username` (string): Nombre de usuario del usuario.
  - `email` (string): Correo electrónico del usuario.
  - `password` (string): Contraseña del usuario.
- **Respuesta Exitosa**:
  - Código de estado: 201 (Created)
  - Cuerpo de respuesta: `{"token": `token`, "user":`Datos del usuario`, "message": "User created successfully!"}`
- **Respuesta en Caso de Error**:
  - Codigo de estado: 400 (Bad request).

### Inicio de Sesión

- **URL**: `/api/authentication/login/`
- **Método HTTP**: `POST`
- **Descripción**: Este endpoint permite a los usuarios iniciar sesión en la plataforma.
- **Parámetros de Entrada**:
  - `email` (string): Correo electrónico del usuario.
  - `password` (string): Contraseña del usuario.  
- **Respuesta Exitosa**:
  - Código de estado: 200 (OK)
  - Cuerpo de respuesta: `{"token":`Bearer token generado,`"refresh:"`Refresh token, `"user":`Datos del usuario, `"message": "Login successfully!"}`
- **Respuesta en Caso de Error**:
  - Codigo de estado: 401 (Unauthorized).

### Información del usuario con sesión iniciada

- **URL**: `/api/authentication/me/`
- **Método HTTP**: `GET`
- **Descripción**: Este endpoint permite a los usuarios autenticados obtener sus datos de perfil.
- **Encabezados de Autenticación**:
  - `Authorization: Bearer [token]` (Reemplaza `[token]` con el token válido)
- **Respuesta Exitosa**:
  - Código de estado: 200 (OK)
  - Cuerpo de respuesta: Datos del usuario (ejemplo: `{"id": 1, "email": "usuario@example.com", "username": "usuario123", ...}`)

### Editar detalles del usuario

- **URL**: `/api/authentication/me/`
- **Método HTTP**: `PUT`, `PATCH`
- **Descripción**: Este endpoint permite a los usuarios autenticados editar sus datos de perfil.
- **Encabezados de Autenticación**:
  - `Authorization: Bearer [token]` (Reemplaza `[token]` con el token válido)
- **Respuesta Exitosa**:
  - Código de estado: 200 (OK)
  - Cuerpo de respuesta: `{"message": "Update successfully!", "user": {"id": 1, "username": "usuario123_update", "email": "usuario_update@example.com", ...}}`)

### Ver el perfil de un usuario

- **URL**: `/api/user/<int:pk>`
- **Método HTTP**: `GET`
- **Descripción**: Este endpoint permite a los usuarios ver el perfil de otros usuarios.
- **Encabezados de Autenticación**:
  - `Authorization: Bearer [token]` (Reemplaza `[token]` con el token válido)
- **Respuesta Exitosa**:
  - Código de estado: 200 (OK)
  - Cuerpo de respuesta: `{"user": {"id", "username": "test1" , "photo_image": "img/", "posts": [], "followers_users": 10}}`
- **Respuesta en Caso de Error**:
  - Codigo de estado: 404 (Not found)
  - Cuerpo de respuesta: `{"error": "User not found"}`

### Cerrar Sesión

- **URL**: `/api/logout/`
- **Método HTTP**: `POST`
- **Descripción**: Este endpoint permite a los usuarios cerrar su sesión en la plataforma.
- **Encabezados de Autenticación**:
  - `Authorization: Bearer [token]` (Reemplaza `[token]` con el token válido)
- **Respuesta Exitosa**:
  - Código de estado: 200 (OK)
  - Cuerpo de respuesta: `{"message": "Logout successfully!"}`


## Salas