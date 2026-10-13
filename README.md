# University Research Opportunity Portal

🔗 **GitHub Repository:** [https://github.com/Hamzachan69/University-Research-Opportunity-Portal](https://github.com/Hamzachan69/University-Research-Opportunity-Portal)

A full-stack web application that allows faculty members to **post, browse, update, and delete** research opportunities at a university. Built with a **FastAPI** (Python) backend, **MySQL** database, and a vanilla **HTML/CSS/JS** frontend styled with Tailwind CSS.

### 📌 Quick Links

| Resource | Location |
|---|---|
| 🎥 Demo Video | [`Demo Video/assignment.mp4`](Demo%20Video/assignment.mp4) |
| 📬 Postman Collection | [`University Research APP.postman_collection.json`](University%20Research%20APP.postman_collection.json) |

---

## Table of Contents

- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Database Setup](#database-setup)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [API Endpoints](#api-endpoints)
- [Postman Collection](#postman-collection)

---

## Project Structure

```
University-Research-Opportunity-Portal/
├── research-portal-backend/
│   ├── main.py                 # FastAPI app with all CRUD routes
│   ├── model.py                # Pydantic schemas (request validation)
│   ├── database.py             # MySQL connection helper
│   ├── schema.sql              # Database schema + sample data
│   ├── test_connection.py      # Quick script to verify DB connectivity
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (DB credentials)
│   └── .gitignore
│
├── research-portal-frontend/
│   ├── index.html              # Main HTML page
│   └── app.js                  # Frontend logic (fetch API calls, DOM)
│
├── University Research APP.postman_collection.json   # Postman collection
└── README.md
```

---

## Tech Stack

| Layer      | Technology                              |
| ---------- | --------------------------------------- |
| Frontend   | HTML, Tailwind CSS (CDN), Vanilla JS    |
| Backend    | Python 3.11, FastAPI, Uvicorn           |
| Database   | MySQL 8.x                               |
| API Client | Postman                                 |

---

## Prerequisites

Make sure the following are installed on your system before proceeding:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **MySQL Server 8.x** — [Download](https://dev.mysql.com/downloads/mysql/)
- **Postman** (optional, for API testing) — [Download](https://www.postman.com/downloads/)
- A modern **web browser** (Chrome, Edge, Firefox)

---

## Database Setup

1. Open a MySQL terminal or client (MySQL Workbench, command line, etc.)

2. Run the schema file to create the database, table, and seed data:

   ```bash
   mysql -u root -p < research-portal-backend/schema.sql
   ```

   Or copy-paste the contents of [`research-portal-backend/schema.sql`](research-portal-backend/schema.sql) into your MySQL client and execute it.

3. Verify the setup:

   ```sql
   USE research_portal;
   SELECT * FROM opportunities;
   ```

   You should see **5 sample rows**.

---

## Backend Setup

1. **Navigate** to the backend directory:

   ```bash
   cd research-portal-backend
   ```

2. **Create a virtual environment** (skip if `venv/` folder already exists):

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the `.env` file**:

   Create a `.env` file in the `research-portal-backend/` directory (if it doesn't exist) with your MySQL credentials:

   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=research_portal
   DB_PORT=3306
   ```

6. **Test the database connection**:

   ```bash
   python test_connection.py
   ```

   Expected output:
   ```
   [SUCCESS] Connected successfully!
   Found 5 rows:
   ...
   ```

7. **Start the backend server**:

   ```bash
   python main.py
   ```

   Or equivalently:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at **http://127.0.0.1:8000**.

   FastAPI auto-generated docs are available at:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

---

## Frontend Setup

The frontend is a static HTML page — no build tools or `npm install` required.

1. Make sure the **backend server is running** (see above).

2. Open `research-portal-frontend/index.html` directly in your browser:

   - Double-click the file, **or**
   - Right-click → "Open with" → your browser, **or**
   - Use the VS Code **Live Server** extension

3. The frontend connects to the backend at `http://127.0.0.1:8000` and will display all research opportunities.

> **Note:** If the backend is not running, the frontend will show a loading state or empty list.

---

## API Endpoints

All endpoints are prefixed with `/api/opportunities`.

| Method   | Endpoint                       | Description                 | Status Codes       |
| -------- | ------------------------------ | --------------------------- | ------------------ |
| `GET`    | `/api/opportunities`           | List all opportunities      | 200                |
| `GET`    | `/api/opportunities/{id}`      | Get a single opportunity    | 200, 404           |
| `POST`   | `/api/opportunities`           | Create a new opportunity    | 201, 400, 500      |
| `PUT`    | `/api/opportunities/{id}`      | Update an opportunity       | 200, 400, 404, 500 |
| `DELETE` | `/api/opportunities/{id}`      | Delete an opportunity       | 200, 404           |

### Sample Request Body (POST / PUT)

```json
{
  "title": "AI for Healthcare Diagnostics",
  "description": "Using deep learning models to detect diseases early.",
  "research_area": "Artificial Intelligence",
  "faculty_name": "Dr. Ahmed Khan",
  "department": "Computer Science",
  "required_skills": "Python, TensorFlow, Data Analysis",
  "available_positions": 2,
  "application_deadline": "2026-12-15",
  "status": "Open"
}
```

### Field Validations

| Field                  | Type    | Rules                             |
| ---------------------- | ------- | --------------------------------- |
| `title`                | string  | Required, min 1 character         |
| `description`          | string  | Required, min 1 character         |
| `research_area`        | string  | Required                          |
| `faculty_name`         | string  | Required                          |
| `department`           | string  | Required                          |
| `required_skills`      | string  | Optional                          |
| `available_positions`  | integer | Required, must be > 0             |
| `application_deadline` | date    | Required, format `YYYY-MM-DD`     |
| `status`               | enum    | `"Open"` or `"Closed"` (default: `"Open"`) |

---

## Postman Collection

A pre-built Postman collection is included in the root of the project:

📄 **`University Research APP.postman_collection.json`**

### How to Import

1. Open **Postman**
2. Click **Import** (top-left)
3. Drag and drop the `.json` file, or click **Upload Files** and select it
4. The collection **"University Research Opportunity Portal"** will appear in your sidebar

### Included Requests

| #  | Request Name             | Method   | URL                                          |
| -- | ------------------------ | -------- | -------------------------------------------- |
| 1  | Get All Opportunities    | `GET`    | `{{base_url}}/api/opportunities`             |
| 2  | Get Opportunity by ID    | `GET`    | `{{base_url}}/api/opportunities/1`           |
| 3  | Create Opportunity       | `POST`   | `{{base_url}}/api/opportunities`             |
| 4  | Update Opportunity       | `PUT`    | `{{base_url}}/api/opportunities/1`           |
| 5  | Delete Opportunity       | `DELETE` | `{{base_url}}/api/opportunities/1`           |

The collection uses a variable `{{base_url}}` set to `http://127.0.0.1:8000`. The POST and PUT requests include pre-filled JSON bodies ready to send.

