# 📖 ArtFolio API Documentation

**Base URL**: `http://localhost:8000/api/v1`

| Resource | Endpoints | Description |
| :--- | :--- | :--- |
| **Auth** | `/auth/` | Register, Login, Token Refresh |
| **Account** | `/account-details` | Manage your own profile (Get, Update, Deactivate) |
| **Users** | `/users/` | Public user profiles & listings |
| **Artworks** | `/artworks/` | Create, browse, update, and delete artworks |

---

## 🔐 Authentication

### 1. Register User

Create a new account.

- **Endpoint**: `POST /auth/register`
- **Status Codes**: `201 Created`, `409 Conflict` (Duplicate email/username)
- **Body** (`application/json`):

```json
{
  "username": "artlover99",
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### 2. Login (Get Access Token)

Authenticate and receive Access & Refresh tokens.

- **Endpoint**: `POST /auth/login`
- **Body** (`application/json`):

  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- **Response**:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "username": "user123"
}
```

### 3. Refresh Access Token

Get a new Access Token using a valid Refresh Token.

- **Endpoint**: `POST /auth/refresh`
- **Body** (`application/json`):

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1Ni..."
}
```

---

## 👤 Account Management (Me)

All endpoints here require header: `Authorization: Bearer <access_token>`

### 1. Get My Details

Fetch your own private profile (includes email).

- **Endpoint**: `GET /account-details`
- **Response**:

```json
{
  "id": "64f1a2b3c9e8...",
  "username": "artlover99",
  "email": "user@example.com",
  "full_name": "Art Lover",
  "bio": "I love painting.",
  "is_active": true,
  "profile_image": "https://res.cloudinary.com/..."
}
```

### 2. Update My Profile

Update profile info and/or upload a new profile picture.

- **Endpoint**: `PATCH /account-details`
- **Body** (`multipart/form-data`):
  - `full_name` (text)
  - `bio` (text)
  - `image` (file)
- **Response**: (Same as Get Details)

### 3. Deactivate Account

Deactivate your account (soft delete).

- **Endpoint**: `PATCH /account-details/deactivate`
- **Response**:

```json
{
  "message": "User account deactivated successfully"
}
```

### 4. Reactivate Account

Reactivate your account.

- **Endpoint**: `PATCH /account-details/reactivate`
- **Response**:

```json
{
  "message": "User account reactivated successfully"
}
```

---

## 👥 Users (Public)

### 1. List Users

Browse active community members.

- **Endpoint**: `GET /users?skip=0&limit=10`
- **Response**:

```json
[
  {
    "id": "64f1a2b3c9e8...",
    "username": "artist_one",
    "full_name": "The Artist",
    "bio": "Digital Creator",

    "profile_image": "https://..."
  },
  ...
]
```

### 2. Search Users

`GET /api/v1/users/search`

Search users by username or full name (fuzzy match).

- **Parameters**: `q` (query) - Search term.
- **Response**: List of User objects.

### 3. Get Public Profile

View a specific user's public details.

- **Endpoint**: `GET /users/{username}`
- **Note**: Does *not* return sensitive info like email.
- **Response**:

```json
{
  "id": "64f1a2b3c9e8...",
  "username": "artist_one",
  "full_name": "The Artist",
  "bio": "Digital Creator",
  "profile_image": "https://..."
}
```

### 4. Get User Artworks

Retrieve all artworks owned by a specific user.

- **Endpoint**: `GET /api/v1/users/{user_id}/artworks`
- **Response**:

```json
[
  {
    "id": "6512b3c...",
    "title": "Sunset",
    "description": "Oil on canvas",
    "image_url": "https://res.cloudinary.com/...",
    "owner": {
      "id": "64f1a2b3c9e8...",
      "username": "artist_one",
      "full_name": "The Artist"
    },
    "created_at": "2023-10-01T12:00:00Z"
  }
]
```

---

## 🎨 Artworks

### 1. Create Artwork

Upload a new piece. Requires Auth.

- **Endpoint**: `POST /artworks`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body** (`multipart/form-data`):
  - `title`: "Sunset" (required)
  - `description`: "Oil on canvas"
  - `image`: (binary file) (required)
- **Response**:

```json
{
  "id": "6512b3c...",
  "title": "Sunset",
  "description": "Oil on canvas",
  "image_url": "https://res.cloudinary.com/...",
    "owner": {
      "username": "artlover99",
      "profile_image": "https://..."
    },
    ...
}
```

### 3. Search Artworks

`GET /api/v1/artworks/search`

Search artworks by title or description.

- **Parameters**: `q` (query) - Search term.
- **Response**:

```json
[
  {
    "id": "6512b3c...",
    "title": "Sunset",
    "description": "Oil on canvas",
    "image_url": "https://res.cloudinary.com/...",
    "owner": {
      "username": "artlover99",
      "profile_image": "https://..."
    },
    "created_at": "2023-10-01T12:00:00Z"
  }
]
```

### 4. Get Artwork Details

View a specific artwork.

- **Endpoint**: `GET /artworks/{id}`
- **Path Param**: `id` (e.g., `6512b3c...`)
- **Response**:

```json
{
  "id": "6512b3c...",
  "title": "Sunset",
  "description": "Oil on canvas",
  "image_url": "https://res.cloudinary.com/...",
  "owner": {
    "username": "artlover99",
    "profile_image": "https://..."
  },
  "created_at": "2023-10-01T12:00:00Z"
}
```

### 5. Update Artwork

Update an artwork you own. Requires Auth.

- **Endpoint**: `PATCH /artworks/{id}`
- **Body** (`multipart/form-data`):
  - `title`: "New Title"
  - `image`: (new file)
- **Response**:

```json
{
  "id": "6512b3c...",
  "title": "New Title",
  "description": "Oil on canvas",
  "image_url": "https://res.cloudinary.com/...",
  "owner": {
    "username": "artlover99",
    "profile_image": "https://..."
  },
  "created_at": "2023-10-01T12:00:00Z"
}
```

### 6. Delete Artwork

Remove an artwork you own. Requires Auth.

- **Endpoint**: `DELETE /artworks/{id}`
- **Response**:

```json
{
  "message": "Artwork deleted successfully"
}
```

---
