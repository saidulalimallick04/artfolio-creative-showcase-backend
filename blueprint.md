# 🗺️ ArtFolio Backend Blueprint

This document outlines the step-by-step development plan for the **ArtFolio API**. The development is divided into 12 logical phases to ensure a structured and efficient workflow.

## 🏗️ Phase 1: Project Initialization & Structure Check

- **Goal**: Set up the development environment and project foundation.
- **Steps**:
    1. Create a virtual environment and activate it.
    2. Install core dependencies (via `uv`): `fastapi`, `uvicorn`, `motor`, `beanie`, `pydantic-settings`, `pyjwt`, `bcrypt`, `python-multipart`, `cloudinary`.
    3. Define the project folder structure:

        ```text
        api/
        └── v1/
            └── endpoints/
        core/ (config, security)
        db/ (connection)
        models/ (beanie models)
        schemas/ (pydantic models)
        tests/
        main.py
        ```

    4. Initialize Git repository (if not already done).

## 🗄️ Phase 2: Database Configuration (MongoDB)

- **Goal**: Establish a connection to the MongoDB database.
- **Steps**:
    1. Create `core/config.py` to handle environment variables (using `pydantic-settings`).
    2. Create `db/mongodb.py` to manage the `AsyncIOMotorClient` and initialize `Beanie`.
    3. Implement startup and shutdown event handlers in `main.py` to connect/disconnect the database.
    4. Verify the connection with a simple ping test.

## 🔐 Phase 3: Core Security & Authentication Logic

- **Goal**: Implement the building blocks for secure authentication.
- **Steps**:
    1. Set up `Passlib` implementation for password hashing and verification.
    2. Implement JWT handling in `core/security.py` using `pyjwt`:
        - Function to create **Access Tokens** (short-lived).
        - Function to create **Refresh Tokens** (long-lived).
    3. Define Pydantic models for `Token` and `TokenData`.

## 🚪 Phase 4: User Registration & Login Endpoints

- **Goal**: Allow users to sign up and authenticate.
- **Steps**:
    1. Define the `User` Pydantic models (UserCreate, UserInDB, UserResponse).
    2. Implement `POST /api/v1/auth/register`:
        - Validate email uniqueness.
        - Hash password.
        - Store user in MongoDB.
    3. Implement `POST /api/v1/auth/login`:
        - Verify credentials.
        - Generate and return Access & Refresh tokens.

## 🔄 Phase 5: Smart Token Rotation & Authorization

- **Goal**: Secure the API and manage session lifecycle.
- **Steps**:
    1. Implement the `get_current_user` dependency to protect routes using the Access Token.
    2. Implement the **Smart Token Rotation** logic:
        - Create endpoint `POST /api/v1/auth/refresh`.
        - Verify the old refresh token.
        - Check if it's nearing expiration (< 2 days).
        - If yes, issue a new one; otherwise, return the existing one.

## 👤 Phase 6: User Profile Management

- **Goal**: Enable fetching user data.
- **Steps**:
    1. Implement `GET /api/v1/users`: List all registered users.
    2. Implement `GET /api/v1/users/{username}`:
        - Fetch user details properties.
        - (Later, this will also include their artworks).

## ☁️ Phase 7: Cloudinary Integration

- **Goal**: Set up image storage solution.
- **Steps**:
    1. Configure Cloudinary keys in `core/config.py`.
    2. Create a service helper `services/cloudinary_service.py`.
    3. Implement a function to upload a file and return the URL.
    4. Implement a function to delete a file (for cleanup).

## 🎨 Phase 8: Artwork CRUD Operations

- **Goal**: Core functionality for managing art pieces.
- **Steps**:
    1. Define `Artwork` Pydantic models (ArtworkCreate, ArtworkResponse).
    2. Implement `POST /api/v1/artworks`:
        - Accept form data + `image` file.
        - Upload image to Cloudinary.
        - Store metadata in MongoDB linked to the current user.
    3. Implement `GET /api/v1/artworks` (Explore page) and `GET /api/v1/artworks/{id}`.
    4. Implement `DELETE /api/v1/artworks/{id}` (Ensure only the owner can delete).

## 🔀 Phase 9: API Versioning & Router Assembly

- **Goal**: Organize endpoints cleanly under versioned paths.
- **Steps**:
    1. Create a version router file (`api/v1/api.py`).
    2. Include Auth, User, Account, and Artwork routers.
    3. Mount this main router to `app` with the prefix `/api/v1` (Managed dynamically in Phase 12).
    4. Ensure all endpoints follow the naming convention defined in `goal.md`.

## 🧪 Phase 10: Validation, Testing & Documentation

- **Goal**: Ensure reliability and readiness for deployment.
- **Steps**:
    1. Add global error handlers for common exceptions (e.g., validation errors, auth errors).
    2. Verify strict Pydantic validation for all inputs.
    3. Test all endpoints using Postman (export implementation for submission).
    4. Polish `README.md` with setup instructions.
    5. Double-check code quality and comments.

## 🛠️ Phase 11: Account Refactoring & Security Hardening

- **Goal**: Dedicate endpoints for profile management and improve token security.
- **Steps**:
    1. Create `api/v1/endpoints/account.py`.
    2. Implement `GET /api/v1/account-details` and `PATCH /api/v1/account-details` (multipart/from-data).
    3. Move deactivation logic to `PATCH /api/v1/account-details/deactivate`.
    4. Remove legacy `/me` endpoints from `users.py`.
    5. Update `Refresh Token` logic to accept JSON body instead of query params.
    6. Ensure `User` lookups use `PydanticObjectId` conversion for robustness.

## 🚀 Phase 12: Generalization & Finalization

- **Goal**: Make the API architecture dynamic and documentation perfect.
- **Steps**:
    1. Refactor `main.py` to support **Dynamic Version Loading**:
        - Automatically scan `api/` directory.
        - Mount routers for `v1`, `v2`, etc. based on folder existence.
    2. Update `README.md` with:
        - Comprehensive architecture report.
        - Strict `.env` requirements list.
    3. Standardize `API_DOCUMENTATION.md` with detailed JSON Request/Response examples for all endpoints.
    4. Finalize `Postman Collection` with new Account endpoints and valid testing variables.

## 🌟 Phase 13: Final Polish & Advanced Features

- **Goal**: Enhance API with search, randomization, and better frontend integration.
- **Steps**:
    1. Implement **Search Endpoints** with Regex support:
        - `GET /api/v1/users/search?q=...`
        - `GET /api/v1/artworks/search?q=...`
    2. Implement **User Portfolio Endpoint**: `GET /api/v1/users/{user_id}/artworks`.
    3. Implement **Account Reactivation**: `PATCH /api/v1/account-details/reactivate`.
    4. **Frontend Optimization**:
        - Include `username` in Login response.
        - Standardize `_id` serialization to `id` globally.
        - **Randomize** the `GET /artworks` feed for dynamic discovery.
    5. **Security/Performance Optimization**:
        - Optimize **Refresh Token** endpoint to exclude `username` from response, avoiding unnecessary database lookups.

## 🏁 Phase 14: System Validation & Final Polish

- **Goal**: Verify end-to-end functionality and prepare for delivery.
- **Steps**:
    1. **Mock Data Generation**:
        - Create and refine `mock_data/populate_db.py`.
        - Generate 100+ Realistic User profiles.
        - Generate 500+ Artworks with Unsplash integration.
        - Ensure fair distribution (everyone gets at least one artwork).
    2. **Final API Documentation Update**:
        - Remove deprecated fields (e.g., `is_artist`).
        - Fix endpoint paths (e.g., remove trailing slashes).
        - Update Postman Collection variables and examples.
    3. **Bug Fixing & QA**:
        - Fix redirect issues on `PATCH /account-details`.
        - Resolve duplication in mock data.
    4. **Submission Preparation**:
        - Final `README.md` review.
        - Ensure all tests pass.

---

## 👨‍💻 Author

| Profile | Developer Name | Role | GitHub | LinkedIn | X |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [![Sami](https://github.com/saidulalimallick04.png?size=75)](https://github.com/saidulalimallick04) | Saidul Ali Mallick (Sami) | Backend Developer & AIML Engineer | [@saidulalimallick04](https://github.com/saidulalimallick04) | [@saidulalimallick04](https://linkedin.com/in/saidulalimallick04) | [@saidulmallick04](https://x.com/saidulmallick04) |

> ❤️ I believe in building impact, not just writing code.
> _💚 Backend Sage signing off.._
---
