Supabase Authentication API

A secure authentication API built with **FastAPI** and **Supabase Auth**. This project implements user signup, login, logout, JWT verification, protected routes, and public routes.

🚀 Technologies

* Python
* FastAPI
* Supabase Auth
* JWT (JSON Web Tokens)
* Pydantic
* python-dotenv
* Uvicorn
* Swagger UI

📁 Project Structure

```text
Auth-Assignment/
│
├── main.py
├── requirements.txt
├── README.md
└── .env                 # Not included in GitHub
```

🔐 Features

* User registration with email and password
* User login
* User logout
* JWT access-token verification
* Protected profile endpoint
* Public information endpoint
* Interactive Swagger API documentation
* Environment variables for Supabase credentials

⚙️ Setup

1. Clone the repository

```bash
git clone https://github.com/Ayesha954-git/Backend-AI-Engineer-Internship.git
cd Backend-AI-Engineer-Internship/Auth-Assignment
```

 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

 4. Configure environment variables

Create a `.env` file inside the `Auth-Assignment` folder:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

Replace the values with your Supabase project credentials.

Never commit the `.env` file to GitHub.

▶️ Run the API

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

📚 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all endpoints directly from Swagger UI.

🔗 API Endpoints

| Method | Endpoint             | Description                      | Authentication |
| ------ | -------------------- | -------------------------------- | -------------- |
| POST   | `/auth/signup`       | Register a new user              | Not required   |
| POST   | `/auth/login`        | Login and receive JWT tokens     | Not required   |
| POST   | `/auth/logout`       | Logout the current user          | Not required   |
| GET    | `/protected/profile` | Get authenticated user's profile | Required       |
| GET    | `/public/info`       | Get public information           | Not required   |

🔑 Authentication Flow

The authentication flow works as follows:

```text
User
 │
 ├── POST /auth/signup
 │       ↓
 │   Supabase creates account
 │
 ├── POST /auth/login
 │       ↓
 │   Supabase returns access token
 │
 └── GET /protected/profile
         ↓
    Authorization: Bearer <access_token>
         ↓
    JWT verified by Supabase
         ↓
    Protected profile returned
```

🛡️ Protected Route

The `/protected/profile` endpoint requires a valid Supabase access token.

The request must include:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

A valid token returns the authenticated user's ID and email.

Requests without a valid token are rejected with:

```text
401 Unauthorized
```

🧪 Testing

The API can be tested using Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

1. Test `/auth/signup`
2. Test `/auth/login`
3. Copy the returned `access_token`
4. Test `/public/info`
5. Test `/protected/profile` without a token
6. Test `/protected/profile` with a valid token
7. Test `/auth/logout`

🔒 Security

Sensitive Supabase credentials are stored in environment variables.

The `.env` file should never be committed or pushed to GitHub.

The project uses JWT access tokens to authenticate requests to protected endpoints.


