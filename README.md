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


### Dynamical Feature
In this project, search commented with ```dynamical features``` keywords, that refer to some code or array should change based on different features like ```fish_type``` or ```pool_type```.

---


## ⚡️ Note: Switch Project to Production Mode

Before running in production, make sure to:


1. **Set environment variable to production:**
	```bash
	export FLASK_ENV=production
	```
2. **Disable debug mode in your code:**
	```python
	app.run(debug=False)
	```
	Or ensure you do not use `debug=True` anywhere.
3. **Install and use a WSGI server (Gunicorn, uWSGI) instead of Flask's built-in server.**
	- Install Gunicorn in your virtual environment:
	  ```bash
	  pip install gunicorn
	  ```
	- Run your app with Gunicorn:
	  ```bash
	  gunicorn main:app --bind 0.0.0.0:5000 --workers 3
	  ```
4. **(Recommended) Apply security best practices:**
	- Enable HTTPS (use Nginx or Caddy as reverse proxy)
	- Set up authentication and authorization for sensitive endpoints
	- Configure CORS if accessed from web clients
	- Use environment variables for secrets (never hardcode)
	- Monitor logs and set up rate limiting if needed

---

## 🚀 Running, Monitoring, and Stopping in Production/VPS

### 1. Running the Project in Production

**Recommended: Use Gunicorn (WSGI server) for production deployments.**

1. Activate your virtual environment:
	```bash
	source .venv/bin/activate
	```
2. Run the app with Gunicorn:
	```bash
	gunicorn main:app --bind 0.0.0.0:5000 --workers 3
	```
	- Replace `main:app` if your Flask app object is named differently or in another file.
	- You can change the port and number of workers as needed.

### 2. Monitoring the Project

**Option A: Simple Log Monitoring**

Check Gunicorn output (if you run it in foreground):
```bash
tail -f gunicorn.log
```

**Option B: Use Supervisor (Recommended for VPS/Server)**

Install supervisor (if not installed):
```bash
sudo apt-get install supervisor
```

Create a config `/etc/supervisor/conf.d/api-forecast-kolam.conf`:
```
[program:api-forecast-kolam]
command=/path/to/.venv/bin/gunicorn main:app --bind 0.0.0.0:5000 --workers 3
directory=/path/to/api-forecast-kolam
autostart=true
autorestart=true
stderr_logfile=/var/log/api-forecast-kolam.err.log
stdout_logfile=/var/log/api-forecast-kolam.out.log
user=yourusername
```

Reload supervisor and start the app:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start api-forecast-kolam
```

Monitor logs:
```bash
tail -f /var/log/api-forecast-kolam.out.log
```

### 3. Stopping the Project

**If using Supervisor:**
```bash
sudo supervisorctl stop api-forecast-kolam
```

**If running Gunicorn manually:**
- Press `Ctrl+C` in the terminal running Gunicorn
- Or kill the process:
  ```bash
  pkill gunicorn
  ```

---

**Tip:** For public access, use Nginx as a reverse proxy to Gunicorn for better performance and HTTPS support.




