User Requirements:
To create a web application using Flask framework to manage inventory of a list of products in respective warehouses. Imaging this application will be used in a shop or a warehouse that needs to keep track of various products and various locations.

Inventory Management Web Application :
In the inventory Shop it contains product,location and product movements and show the Transactions Report.
•	I Had Successfully created the product.html page in that the user can add product name and Quantity if they wants to modify they can do in that pages.
•	In Location page  as successfully add their Location and modify in the Locations in Location.html
•	I had created product movement.html for showcasing the Transactions and Transaction history in that page.

Features I’m Added:
•	Login and Signup(By Hashing technique)
•	Search in Transactions by product name or Warehouse.
•	Easy Navigations
•	Using Sqlite Database.
•	Can easily Modify The Product Details and Location Details.
•	Bootstrap Styles are Used in Web pages.

File Paths:
├── aerele\
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models (Product, Location, ProductMovement, User)
│   ├── routes.py            # Application routes and logic
│   ├── templates\           # HTML templates for the app
│   │   ├── signup.html      # Signup page template
│   │   ├── login.html       # Login page template
│   │   ├── product.html     # Product listing page
│   │   ├── location.html    # Location listing page
│   │   ├── movement.html    # Product movement page
│   │   ├── edit_product.html # Edit product page
│   │   ├── edit_location.html # Edit location page
│   │   ├── search_results.html # Search results page
│   ├── static\              # Static files (CSS, JS, images)
│   │   ├── back.jpg         # Background image
├── migrations\              # Database migration files
│   ├── versions\            # Individual migration scripts
│   │   ├── ...              # Migration file
├── requirements.txt         # Python dependencies
├── config.py                # Configuration file (if applicable)
└── run.py                   # Entry point to run the Flask app

Steps To Run the Application:
Step1: Extract the Zip File 
Step2: Migrate the Sqlite Database in Your System
•	flask --app aerele db init
•	flask --app aerele db migrate -m "Initial migration"
•	flask --app aerele db upgrade
Step 3: Import the Necessary Flask files in cmd.
Step 4: Run the Application 
•	python appname.py(python app.py)


Screenshots:
1.	First it Ask the User Details to Allow in Inventory Shop.
![image](https://github.com/user-attachments/assets/7365d8fc-a817-498e-8fa4-463a930bb7e0)
2.If the user details Are correct it will navigate to Base.html File
![image](https://github.com/user-attachments/assets/9d2fa732-018b-4429-91c7-25cb2eddeff0)
3.After that we can add the products in product.html
![image](https://github.com/user-attachments/assets/085bd2f4-fcbc-47d3-b042-4ce4b035fe51)
4.In sidebar if we click the Location It will navigate to the Location page and show the Available Locations I we need to Add Any new Locations.
![image](https://github.com/user-attachments/assets/f4e92e22-37ef-4b1b-a68c-051b6788f68a)
It Successfully Added the New Location Thiruvannamalai
![image](https://github.com/user-attachments/assets/e6bb789c-e0ff-439a-b686-dfdb705bec1b)
5.Products Movements (Make Transactions and Available balances in Hub and Transaction History)
There are three type Of Transactions
1.Unknown to Hub (it reduces the Original product Quantity)
Example: I’m entered tomato As 100 Quantity
![image](https://github.com/user-attachments/assets/9800b323-4e8b-408b-8efd-b484bf45ce46)
I am moving 50 Quantity in(unknown to Hub) Transaction
![image](https://github.com/user-attachments/assets/fefa21a5-2056-43ac-9909-42cf1eecc626)
It successfully Transferred to Hub And shown in product balances and updated in Transaction history.
![image](https://github.com/user-attachments/assets/5865206e-3bf6-47ed-9ccf-b3a6e341f9a3)
It also updated Remaining Available Quantity in product page I moved 50 quantity the Remaining will be updated successfully.
![image](https://github.com/user-attachments/assets/7ca2cdad-652c-4266-9144-d2b7f1eb5e05)

 Type 2:(Hub to Hub)
In Hyderabad hub contains 50 quantity I move the 25 quantity to Coimbatore Hub.
![image](https://github.com/user-attachments/assets/fab2ee8c-0ee2-481a-a0a6-e2b53f12f272)
it successfully transferred Hyderabad hub to Coimbatore hub.
![image](https://github.com/user-attachments/assets/a92e1acd-910a-428e-8699-d0c2251e62c1)
Type 3:(Hub to Consumer)
The Coimbatore hub Contains 25 quantity I want to sell 20 Quantity to consumer .
![image](https://github.com/user-attachments/assets/08d2ae89-0d6e-468a-9e8e-cb141c98344c)

It successfully updated Coimbatore hub quantity as 5 and the product is selled in Coimbatore.


If we want to search the transaction history by product or Ware House:
Example :in search box I’ll entered “Tom” and click entered the result page will show like this.
![image](https://github.com/user-attachments/assets/b92cf326-1346-4e9b-9a7e-f7d6ad0d3f9d)

Hence all the Actions are done in the given Requirements and I add the few more features for user Flexibility .

Referances:
1.Bootsrap Styles – For user interface and styling.
2.For Developing This Application – WaterFall model in (OOSE-CCS356 (Anna University))
•	This model the Development starts Requirements gathering phase.
•	Then process analysis,design,coding,testing and Maintenance.



