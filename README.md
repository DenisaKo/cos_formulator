# 🧪 CosFormulator

**CosFormulator** is a simple and practical Django web application that allows users to create and manage cosmetic formulations. Users can select ingredients, specify their usage percentages, and keep track of their compositions.

This project was developed as part of IU’s course *Project: Java and Web Development (DLBCSPJWD01)* at **IU International University of Applied Sciences**.

---

## ✨ Features

✅ User authentication (Sign up & Login)  
✅ Create chemical materials as cosmetic ingredients  
✅ Create formulations by selecting ingredients and specifying their percentages.  
✅ Live percentage recalculation and safety check   
✅ Responsive web interface using Django templating  
✅ Initial data for ingredients is included for demonstration

---


## 🚀 Tech Stack 
- **Front-end**: Vanilla JavaScript
- **Back-end**: Phyton (Django)
- **Database**: SQLite
- **Styling**: Tailwind CSS + Flowbite

## 🛠️ Installation and Setup Guide

Follow these steps to set up the project locally.

### **1. Clone the repository**  
```sh
git clone https://github.com/DenisaKo/cos_formulator
cd cos_formulator
```

### **2. Create virtual environment and activate it**  
```sh
python3 -m venv venv
source venv/bin/activate
```

### **3. Install dependencies**  
```sh
pip install -r requirements.txt
```

### **4. Run database migtations**
```sh
python3 manage.py migrate
```
New SQLite database file will be created.


### **5. Create a superuser (optional)**
```sh
python3 manage.py createsuperuser
```
Follow instructions and enter username, email and password


### **6. Pre-populate database with a few sample cosmetic ingredients**
```sh
python3 manage.py loaddata ingredients/ingredients.json
```


### **6. Start the development server**  
```sh
python3 manage.py runserver
```
App will be available at **http://127.0.0.1:8000/**  


### **7. Stop the app after use** 

- stop the server (contol+c) and deactivate the virtual environment
```sh
deactivate
```


## 📜 License

This project is for educational purposes. Feel free to use and extend it under the terms of the MIT License.

---

## 👩‍💻 Author

Developed by **Denisa**, chemical engineer and software enthusiast, as part of a university project at **IU International University of Applied Sciences**.