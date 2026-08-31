
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client
import os

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI app
app = FastAPI()


# Request model for signup and login
class SignupRequest(BaseModel):
    email: str
    password: str


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Auth API is running",
        "supabase_configured": True
    }


# =========================
# SIGNUP
# =========================

@app.post("/auth/signup")
def signup(user: SignupRequest):
    response = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password
    })

    return {
        "message": "Signup successful",
        "user": response.user
    }


# =========================
# LOGIN
# =========================

@app.post("/auth/login")
def login(user: SignupRequest):
    response = supabase.auth.sign_in_with_password({
        "email": user.email,
        "password": user.password
    })

    return {
        "message": "Login successful",
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": response.user
    }


# =========================
# LOGOUT
# =========================

@app.post("/auth/logout")
def logout():
    supabase.auth.sign_out()

    return {
        "message": "Logout successful"
    }


# =========================
# JWT VERIFICATION
# =========================

def verify_token(authorization: str):
    # Check if Authorization header exists
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required"
        )

    # Check Bearer format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    # Extract token
    token = authorization.split(" ")[1]

    try:
        # Ask Supabase to verify the access token
        response = supabase.auth.get_user(token)

        # Check whether a user was returned
        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return response.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# =========================
# PROTECTED PROFILE
# =========================

@app.get("/protected/profile")
def profile(authorization: str = Header(None)):
    # Verify JWT token
    user = verify_token(authorization)

    return {
        "message": "Protected profile",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


# =========================
# PUBLIC INFO
# =========================

@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint",
        "authentication_required": False
    }
