# 🎨 ArtFolio Backend API

> **Objective**: Build a robust, scalable backend system for a creative portfolio application, enabling artists to showcase their work and connect with a community.

## 🚀 Overview

ArtFolio is a production-ready RESTful API built with **FastAPI** and **MongoDB** (using Beanie ODM). It features a modern, automated architecture supporting dynamic API versioning, robust authentication, and seamless media management via Cloudinary.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB (Beanie ODM + Motor Driver)
- **Authentication**: OAuth2 with JWT (Access + Refresh Tokens)
- **Security**: Passlib (Bcrypt), Pydantic V2 Validation
- **Storage**: Cloudinary (Multipart Image Uploads)
- **Testing**: Pytest (AsyncIO)
- **Package Manager**: uv
- **Architecture**: Modular, Dynamic Version Loading

## ⚡ Key Features

### 🔐 Authentication & Security

- **Secure JWT Flow**: Short-lived Access Tokens (def: 30m) and strictly validated Refresh Tokens (def: 7d).
- **Smart Token Rotation**: Refresh tokens are rotated if they are close to expiration to prevent indefinite access.
- **Secure Handling**: Refresh Tokens are accepted via JSON body (not query params) to prevent leakage in server logs.

### 👤 User & Account Management

- **Unified Account Logic**: Single user model for both Artists and Viewers.
- **Account Details**: Dedicated `/account-details` endpoints for retrieving and updating profile info using `multipart/form-data` (Text + File).
- **Deactivation**: Users can deactivate their own accounts without complete deletion.

### 🖼️ Artwork Management

- **Full CRUD**: Create, Read, Update, Delete artworks.
- **Media Support**: Integrated Cloudinary upload for artwork images.
- **Ownership Security**: Strict checks ensure only the artwork creator can update or delete their work.
- **Smart Updates**: `PATCH` endpoints allow updating metadata (Title, Desc) and valid image files simultaneously.

### ⚙️ Scalable Architecture

- **Dynamic API Loading**: `main.py` automatically discovers and mounts API versions (e.g., `v1`, `v2`) from the `api/` directory.
- **Environment Driven**: All critical configurations (Database Name, Secrets, API Keys) are enforced via `.env`.

## 📂 Project Structure

```text
├── api/
│   ├── deps.py               # Dependency Injection (User, Token)
│   └── v1/                   # Version 1 API Package
│       ├── api.py            # V1 Router Aggregator
│       └── endpoints/        # Routes: Auth, Account, Users, Artworks
├── core/
│   ├── config.py             # Strict Environment Settings
│   └── cloud.py              # Cloudinary Helpers
├── db/
│   └── mongodb.py            # Database Connection & Beanie Models
├── models/                   # Beanie ODM Models (User, Artwork)
├── schemas/                  # Pydantic Schemas
├── main.py                   # Application Entry (Dynamic Loader)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- MongoDB (Running locally or Atlas)
- Cloudinary Account
- `uv` (recommended) or `pip`

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/saidulalimallick04/artfolio-creative-showcase-backend.git
   cd artfolio-creative-showcase-backend
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root. **All fields are required**:

   ```env
   # API & Security
   SECRET_KEY=MEOW_MEOW_SECRET_KEY
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7

   # Database
   MONGODB_URL=mongodb://localhost:27017
   DB_NAME=artfolio

   # Cloudinary (Image Hosting)
   CLOUDINARY_CLOUD_NAME=MEOW_MEOW_CLOUD_NAME
   CLOUDINARY_API_KEY=MEOW_MEOW_API_KEY
   CLOUDINARY_API_SECRET=MEOW_MEOW_API_SECRET
   ```

3. **How to Run**

   ### 3.1. Recommended (using uv)

   If you have `uv` installed, this is the fastest way to get started.

      **3.1.1. Install Dependencies & Sync Environment**

      ```bash
      uv sync
      ```

      **3.1.2. Run the Application**

      ```bash
      uv run uvicorn main:app --reload
      ```

      **3.1.3. Run Tests**

      ```bash
      uv run pytest
      ```

   ### 3.2. Alternative (using pip)

   Standard Python workflow using virtual environments.

      **3.2.1. Create and Activate Virtual Environment**

      ```bash
      # Windows
      python -m venv venv
      .\venv\Scripts\activate

      # macOS/Linux
      python3 -m venv venv
      source venv/bin/activate
      ```

      **3.2.2. Install Dependencies**

      ```bash
      pip install -r requirements.txt
      ```

      **3.2.3. Run the Application**

      ```bash
      uvicorn main:app --reload
      ```

      **3.2.4. Run Tests**

      ```bash
      pytest
      ```

- **Swagger UI**:  [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 👨‍💻 Author

| Profile | Developer Name | Role | GitHub | LinkedIn | X |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [![Sami](https://github.com/saidulalimallick04.png?size=75)](https://github.com/saidulalimallick04) | Saidul Ali Mallick (Sami) | Backend Developer & AIML Engineer & Team Lead | [@saidulalimallick04](https://github.com/saidulalimallick04) | [@saidulalimallick04](https://linkedin.com/in/saidulalimallick04) | [@saidulmallick04](https://x.com/saidulmallick04) |

> ❤️ I believe in building impact, not just writing code.
> _💚 Backend Sage signing off.._
---
