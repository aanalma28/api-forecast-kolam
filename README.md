# 🚀 How to Run This Project Locally

This project was originally developed on [Replit](https://replit.com) and uses `uv.lock` for dependency management. Follow the steps below to run it on your local machine.

---

## 📥 Step 1: Clone the Repository

Clone this project from GitHub:

```bash
git clone https://github.com/aanalma28/api-forecast-kolam.git
cd api-forecast-kolam
```

## 🐍 Step 2: Set Up a Virtual Environment

Make sure Python is installed (recommended: Python 3.8 or higher).

### For Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

### For MacOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## 📦 Step 3: Install Dependencies

You can follow step below carefully.

### 1. Install uv
```bash
pip install pipx
pipx install uv
```
### 2. Use uv to create a virtual environment and install dependencies:
```bash
uv venv
uv pip install -r requirements.txt   # if a requirements.txt exists
# or just run your code with:
uv pip install .
```

## ▶️ Step 4: Run the Project

After all dependencies is installed, you can run main.py:

```bash
uv run python main.py
```
you can also use
```bash
python main.py
```



