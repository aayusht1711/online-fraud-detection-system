# 🚀 Running Project Aegis in Visual Studio Code

This guide provides step-by-step instructions to open, run, and debug **Project Aegis** inside **Visual Studio Code**.

---

## ⚡ Option 1: Quick Start (1 Click in VS Code)

1. **Open the Project Folder in VS Code:**
   * Open VS Code.
   * Go to **File > Open Folder...** (`Ctrl + K, Ctrl + O`).
   * Select `c:\Users\dell\Desktop\project 2` and click **Select Folder**.
   *(Or from terminal, run: `code "c:\Users\dell\Desktop\project 2"`)*

2. **Run the Project:**
   * Press **`F5`** (or go to the **Run and Debug** tab on the left sidebar: `Ctrl + Shift + D` and click the green **Play ▶** button next to **"Project Aegis: Run Flask Server"**).
   * VS Code will open the integrated terminal and start the server:
     ```text
     * Running on http://127.0.0.1:5000
     ```

3. **Open the Dashboard in your Browser:**
   * Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 🛠️ Option 2: Run via VS Code Terminal

1. Open the integrated terminal in VS Code:
   * Shortcut: **``Ctrl + ` ``** (Ctrl + Backtick) or **Terminal > New Terminal**.
2. Run the start command:
   ```powershell
   .\.venv\Scripts\python.exe src/app.py
   ```
   *(Or simply run: `.\run.bat`)*

---

## 📦 Python Virtual Environment Details

The project has a pre-configured, self-contained virtual environment:
* **Interpreter Path:** `c:\Users\dell\Desktop\project 2\.venv\Scripts\python.exe`
* **Python Version:** 3.11.9
* **Pre-installed Dependencies:**
  * Flask 3.1.3
  * XGBoost 3.2.0
  * Scikit-Learn 1.9.0
  * Pandas & NumPy
  * Requests & FPDF2

### If You Need to Reinstall or Update Packages:
Open VS Code terminal and run:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
*(Or double-click `install_requirements.bat`)*

---

## 🐞 Pre-Configured VS Code Profiles (`.vscode/launch.json`)

Inside the **Run and Debug** menu (`Ctrl + Shift + D`), you have 3 pre-built profiles:

| Profile Name | Description |
| :--- | :--- |
| **`Project Aegis: Run Flask Server`** | Standard execution of the main dashboard on port 5000. |
| **`Project Aegis: Debug Flask App (Module)`** | Flask debug mode with line-by-line breakpoints and variable inspection. |
| **`Project Aegis: Test Bot CSV Telemetry`** | Runs the automated batch evaluation of `honeypot_login_telemetry.csv`. |

---

## 🛑 Stopping the Server

* In the VS Code terminal where the server is running, press **`Ctrl + C`**.
* Or click the red **Stop ⏹** button in the debug toolbar at the top.
