# 🚀 How to Run This Project Locally

This project was originally developed on [Replit](https://replit.com) and uses `uv.lock` for dependency management. Follow the steps below to run it on your local machine.

---

## 📥 Step 1: Clone the Repository

Clone this project from GitHub and Make sure Python is installed (recommended: Python 3.8 or higher).

```bash
git clone https://github.com/aanalma28/api-forecast-kolam.git
cd api-forecast-kolam
```

## 📦 Step 2: Install Dependencies

You can follow step below carefully.

### 1. Install pipx
```bash
pip install pipx
```
or install user-level globally in machine
```bash
python3 -m pip install --user pipx --break-system-packages
```
### 2. Set pipx in your PATH and install uv
```bash
python3 -m pipx ensurepath
source ~/.bashrc    # or ~/.zshrc

# install uv
pipx install uv
```
### 3. Use uv to create a virtual environment and install dependencies:
 This virtual environment make sure to have independently dependency in virtual machine (VM) or VPS, because this venv didn't install in global environment in machine and potentially causing crash or overwrite other dependency project.
```bash
# ensure you're in the project root
cd /path/to/api-forecast/kolam

# create virtual environment inside the project folder
uv venv

# Install from requirements.txt if exists
uv pip install -r requirements.txt   # if a requirements.txt exists

# or Install project dependencies from pyproject.toml + uv.lock
uv pip install .
```

## ▶️ Step 3: Run the Project

After all dependencies is installed, you can run ```main.py```:

```bash
uv run python main.py
```
If you use FastAPI/Uvicorn, for example:
```bash
uv run uvicorn app:main --host 0.0.0.0 --port 8000 --reload
```

## 4. (Optional) Use Environment Variables
Create ```.env``` file in the project root:
```env
DB_URL=postgresql://...
SECRET_KEY=supersecret
```
Make sure your code uses:
```python
from dotenv import load_dotenv
load_dotenv()
```
Install it with:
```bash
uv pip install python-dotenv
```

## 🔁 Updating Dependencies (if needed)
If you edit ```pyproject.toml```, regenerate the lockfile with:
```bash
uv pip install -e .
uv pip freeze > requirements.txt   # optional legacy support
```
Or recreate ```.venv``` entirely:
```bash
rm -rf .venv
uv venv
uv pip install .
```

## 🧼 Cleanup
To remove the environment:
```bash
rm -rf .venv
```

## 📦 Deploy Automation (Optional)
You can automate this setup with a ```setup.sh```:
```bash
#!/bin/bash
cd "$(dirname "$0")"

# Ensure pipx and uv are installed
python3 -m pip install --user pipx --break-system-packages
python3 -m pipx ensurepath
source ~/.bashrc
pipx install uv

# Setup project
uv venv
uv pip install .

echo "✅ Project ready to run!"
```

## 🔐 Security Reminder
- Never commit ```.env``` or ```.venv``` to Git.
- Always use separate database users per project on production.




