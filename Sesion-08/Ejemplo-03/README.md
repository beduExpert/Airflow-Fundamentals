# Ejemplo #3 - Administración de Permisos

## Objetivo

* Creación de usuarios con diferentes roles

## Desarrollo

![image](/Sesion-08/Ejemplo-03/assets/img/list_users.png)

### Observador

1. Usamos la interfaz web para mostrar la lista de usuarios `Security > List Users`

2. Hacemos click en el botón [+]

    ![image](/Sesion-08/Ejemplo-03/assets/img/add_user.png)

3. Creamos el usuario `observador`
4. Seleccionamos el rol `Viewer`
5. Capturamos los campos *obligatorios y lo activamos
6. Guardamos los cambios y cerramos la sesión
7. Iniciamos sesión con el nuevo usuario `observador`
8. Explora las opciones del menú a las que tienes acceso y las acciones restringidas.

### Operador

1. Iniciar sesión con el usuario administrador: `airflow`
2. Agregar el usuario `operador` bajo el rol `Op`
3. Iniciar sesión con el nuevo usuario `operador`
4. Expolar las opciones del menú disponibles y las acciones restringidas.

### User

1. Iniciar sesión con el usuario administrador: `airflow`
2. Agregar el usuario `usuario` bajo el rol `User`
3. Iniciar sesión con el nuevo usuario `usuario`
4. Expolar las opciones del menú disponibles y las acciones restringidas.

