# Django Project

## Installation and Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Create and Activate a Virtual Environment
#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runsslserver 0.0.0.0:8000
```

### 6. Open in Browser
Go to:
```
https://localhost:8000

```

### 7. Clone Frontend Repository
run npm run dev

### 8. Now You can view the application at 
http://localhost:3000/login
