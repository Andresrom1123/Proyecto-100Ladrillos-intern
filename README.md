# Proyecto 100 ladrillos

## Solución del proyecto
Utilice django para la creación del proyecto.
Como tal la arquictectura que pensaba hacer era la MVC, aunque no utilice como tal un controlador ya que toda la logica la implemente en la vista de la
aplicación.

Hice uso algo básico de docker para concectarme a pgadmin y utilizar postgress.
Considere dividir el proyecto en 2 partes una el login en donde me enfoque en ingresar solamente la tarjeta de débito y su nip.
La otra parte fue el "Menu principal" en donde implemente todas las acciones del menú principal.

En cuestión de tablas de base de datos solamente considere crear una  una tabla llamandola "BankAccount" en la cual tiene los siguientes campos
- debit de tipo string
- nip de tipo string
- amount de tipo int
- locked de tipo booleano
- nip_incorrect de tipo int

Utilice los fixtures para cargar las tarjetas de debito que se me solicitan con sus respectivos nip.
Tambièn aplique algunos test, todos refierendome a ellos con un caso positivo.

## Pasos para correr el proyecto

1. Crear un entorno virtual con python
> Yo utilizo el virtualvenv que trae python https://docs.python.org/es/3/library/venv.html
```
python3 -m venv myvenv
```
![Screenshot from 2023-01-31 07-18-28](https://user-images.githubusercontent.com/53199747/215771441-b91b2c59-0bcb-4d44-af94-87a46172a5ae.png)

2. Activar el entorno virtual.
![Screenshot from 2023-01-31 07-20-41](https://user-images.githubusercontent.com/53199747/215771698-2d760c64-545d-47be-bdce-aa9a78d20cbd.png)
> Recuerda ejecutar todo en el virtualenv. Si no ves un prefijo `(myvenv)` en tu consola tienes que activar tu virtualenv.
Basta con escribir `myvenv\Scripts\activate` en Windows o `source myvenv/bin/activate` en Mac OS / Linux.

3. Instalar las dependencias del proyecto
```
pip install -r requirements.txt
```
4. Crear los contenederos de pgadmin4 y postgres
```
docker-compose up
```
5. Registrar un servidor de postgres con pgadmin4
  - Logearnos en pgadmin4 
    1. Abrimos un navegador y vamos a localhost
    ![Screenshot from 2023-01-31 06-48-09](https://user-images.githubusercontent.com/53199747/215764288-752c210d-fc21-43cc-9998-952071d03102.png)
    2. Va aparecernos un formulario de correo ponemos:
    ```
    admin@admin.com
    ```
    - Contraseña
    ```
    admin
    ```
  - Registrar un nuevo servidor
    1. Dentro del panel de pgadmin4 en la parte izquierda vamos a registrar un nuevo servidor, dando click derecho a **Servers** > **Register** > **Server**
    ![Screenshot from 2023-01-31 06-55-45](https://user-images.githubusercontent.com/53199747/215766030-2a1d070c-8a31-46a5-b453-ec9fb070ef88.png)


    2. Al dar click en server nos saldra un modal
    ![Screenshot from 2023-01-31 07-00-51](https://user-images.githubusercontent.com/53199747/215766788-396c43d3-4ccd-4022-806c-7efef9301fed.png)
    > En **name** podemos poner cualquier nombre
		>
    > Después nos dirigimos en el mismo modal a **Connection**
     ![Screenshot from 2023-01-31 07-04-32](https://user-images.githubusercontent.com/53199747/215767757-c37f1923-2bf3-4686-b5eb-1577e1a98b5e.png)
    > En **Host name** ponemos postgres, cambiamos el **username** por root y en **password** también ponemos root por ultimo guardamos dando click en
    **save**
    
6. Ejecutar las migraciones de tablas del proyecto 
```
python3 manage.py migrate
```
7. Cargar las fixtures del proyecto
```
python3 manage.py loaddata bank_accounts/fixtures/fixtures
```
8. Correr el servidor
```
python3 manage.py runserver
```
9. Correr los test unitarios
```
python3 manage.py test
```
## Probar el proyecto
> Para probar el proyecto en todo momento debe de estar corriendo el servidor y los contenedores de docker y pgadmin4
1. Se puede probar ejecutando los test unitarios con
```
python3 manage.py test
```

Otra manera de probarlo es haciendo uso de alguna herramiento como postman, las rutas, metodos y datos que utilice son los siguientes:
- ```http://localhost:8000/api/v1/bank/login/``` METHOD: POST, data: debit, nip
- ```http://localhost:8000/api/v1/bank/debits/``` METHOD: GET
- ```http://localhost:8000/api/v1/bank/deposit/<account_debit>/``` METHOD: POST, data: deposit
- ```http://localhost:8000/api/v1/bank/withdraw/<account_debit>/``` METHOD: POST, data: withdraw
- ```http://localhost:8000/api/v1/bank/balance/<account_debit>/``` METHOD: GET
- ```http://localhost:8000/api/v1/bank/transfer/<account_debit>/``` METHOD: POST, data: debit, amount

