## Prepare the virtual environment and install all dependencies using the following commands: 
1. cd LittleLemon 
2. pipenv shell
3. pipenv install
4. python manage.py makemigrations
5. python manage.py migrate
6. Activate virtual environment:
   - lemonenv/Scripts/activate
7. python manage.py runserver

## Creating User groups in Django admin panel
1. Create a superuser
   - python manage.py createsuperuser
2. Run server 
   - python manage.py runserver
3. Login to the admin page
   - http://127.0.0.1:8000/admin/
4. Create the following two user groups and then create some random user and assign them to these groups
   from the Django admin panel
      - Manager
      - Delivery crew
   Users not assigned to a group will be considered customers.

## Using Postman or a similar application to access the following API endpoints

### User registration and token generation endpoints
| Endpoint  | Role  | Method  | Purpose  |Sample Request Body |
| :----------:  | :----------: | ----------: |:--------:| :-----------:| 
| /api/users/  | No role required | POST  | Creates a new user with name, email and password | { username: "kelly", email: "kelly@littlemon.com", password: "pass@word123", password_confirmation: "pass@word123"}
| /api/users/uesrs/me/ | Anyone with a valid user token | GET     | Displays only the current user |
| /token/login/ | Anyone with a valid username and password     | POST | Generates access tokens that can be used in other API calls in this project | { username: "kelly", password: "pass@word123" }

   
### Menu-items endpoints
| Endpoint | Role | Method | Purpose | Sample Request Body |
| :----------  | :----------: | ----------: |:--------:| :-----------:| 
| /api/menu-items/ | Customer, delivery crew | GET  | List all menu items. Return a 200 - Ok HTTP status code | 
| /api/menu-items/ | Customer, delivery crew | POST, PUT, PATC, DELETE | Denies access and returns 403 - Unauthorized HTTP status code | {"title": "Coke","price": "2.50","featured": true,"category": 3}
| /api/menu-items/{menuItem}/ | Customer, delivery crew | GET | Lists single menu item 
| /api/menu-items/{menuItem}/ | Customer, delivery crew | POST, PUT, PATCH, DELETE | Returns 403 - Unauthorized
| /api/menu-items/ | Manager | GET | Lists all menu items
| /api/menu-items/ | Manager | POST | Creates a new menu item and returns 201 - Created | { "title": "Cuban Sofrito Chicken Bowl","price": "18.00","featured": true,"category": 1 }
| /api/menu-items/{menuItem}/ | Manager | GET | List single menu item
| /api/menu-items/{menuItem}/ | Manager | PUT, PATCH | Updates single menu item | PUT: { "title": "Cuban Sofrito Chicken Bowl","price": "15.00","featured": true,"category": 1 }, PATCH: { "price" : 20.00 }
| /api/menu-items/{menuItem}/ | Manager | DELETE | Deletes menu item | 
   

### User group management endpoints
| Endpoint     | Role         | Method      | Purpose  |Sample Request Body |
| :----------  | :----------: | ----------: |:--------:| :-----------:| 
| /api/groups/manager/users/  | Manager | GET  | Returns all managers | 
| /api/groups/manager/users/ | Manager | POST | Assigns the user in the payload to the manager group and return 201-Created | {"username":"charles"}
| /api/groups/manager/users/{userId}/ | Manager | DELETE | Removes the particular user from the manager group and returns 200 - Success if everything is okay. If the user is not found, returns 404-NotFound
| /api/groups/delivery-crew/users/ | Manager | GET | Returns all delivery crew |
| /api/groups/delivery-crew/users/ | Manager | POST | Assigns the user in the payload to delivery crew group and return 201-Created HTTP status code | {"username":"charles"}
| /api/groups/delivery-crew/users/{userId}/ | Manager | DELETE | Removes the user from the manager group and returns 200-Success if everything is okay. If the user is not found, return 404-NotFound HTTP status code

### Cart management endpoints
| Endpoint     | Role         | Method      | Purpose  |Sample Request Body |
| :----------  | :----------: | ----------: |:--------:| :-----------:| 
| /api/cart/menu-items/  | Customer | GET  | Returns current items in the cart for the current user token | 
| /api/cart/menu-items/ | Customer | POST | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items |{"menuitem": 4,"quantity": 2}
| /api/cart/menu-items/ | Customer | DELETE | Deletes all menu items created by the current user token |
   
### Order management endpoints
| Endpoint     | Role         | Method      | Purpose  |Sample Request Body |
| :----------  | :----------: | ----------: |:--------:| :-----------:| 
| /api/orders/ | Customer | GET | Returns all the orders with order items created by this user | user token in header
| /api/orders/ | Customer | POST | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. | user token in header &  {"delivery_crew": null, "status": 0}
| /api/orders/{orderId}/ | Customer | GET | Returns all items for this order id. If the order ID doesn't belong to the current user, it displays an appropriate HTTP error status code. | user token in header
| /api/orders/ | Manager | GET |Returns all orders with order items by all users | user token in header
| /api/orders/{orderId} | Customer | PUT, PATCH | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order adn status = 1, ite means the order has been delivered. | mananger token in header
| /api/orders/{orderId} | Manager | GET | Deletes this order | manager token in header
| /api/orders | Delivery crew | GET | Returns all orders with order itmes assigned to the delivery crew | delivery crew token in header
| /api/orders/{orderId} | Delivery crew | PATCH | A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order | delivery crew token in header & {"status": 1}

### Category endpoints
| Endpoint     | Role         | Method      | Purpose  |Sample Request Body |
| :----------  | :----------: | ----------: |:--------:| :-----------:| 
| /api/categories/ | Customer | GET | Returns all the categories | user token in header
| /api/categories/{categoryId} | Customer | GET | Returns a specific category | user token in header
| /api/categories/ | Admin | POST | Creates a new category | admin token in header; {"title":"Tests","slug":"tests"}
| /api/categories/{categoryId} | Admin | PUT | Updates a category | admin token in header;  {"title":"Titles", "slug": "titles"}
| /api/categories/{categoryId} | Admin | DELETE | Deletes a category | admin token in header

