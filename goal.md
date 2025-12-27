# 🎯 REST Backend Project: "ArtFolio API"

> **Objective**: Build a robust, scalable backend system for a creative portfolio application, enabling artists to showcase their work and connect with a community.

## 🚀 Core Features

- **User & Artist Management**: Securely handle user registration, login, and profile management.
- **Advanced JWT Authentication**: Implement a secure, stateless dual-token architecture:
  - **Access Tokens**: Short-lived tokens for authorizing API requests.
  - **Refresh Tokens**: Long-lived tokens used solely to requests new access tokens via a dedicated endpoint (e.g., `/refresh`).
  - **Smart Token Rotation**: The refresh token itself is only rotated (replaced with a new one) if it is nearing expiration (e.g., less than 2 days remaining). Otherwise, the existing refresh token is returned. This "Smart Rotation" strategy balances strict security with database efficiency by reducing unnecessary write operations.
- **Artwork & Media Handling**:
  - Seamlessly upload and manage artwork images using Cloudinary for efficient storage and delivery.
  - Implement full CRUD (Create, Read, Update, Delete) functionality for artworks.
- **Database Integration**: Utilize MongoDB to store user profiles and artwork metadata.
- **API Versioning**: Introduce versioning (e.g., `/v1/`, `/v2/`) to allow for non-breaking changes.

## 🛠️ Technologies

- **Language & Framework**: Python with FastAPI for high-performance, asynchronous API development.
- **Database**: MongoDB (NoSQL, Document-based) for flexible and scalable data storage.
- **Media Storage**: Cloudinary for robust cloud-based image and video management.

## 🔀 API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Create a new user account.
- `POST /api/v1/auth/login`: Authenticate a user and receive a JWT.

### Artists / Users

- `GET /api/v1/users`: Retrieve a list of all users.
- `GET /api/v1/users/{username}`: Fetch a specific user's profile and their artworks.

### Artworks

- `POST /api/v1/artworks`: Upload a new artwork (includes image upload to Cloudinary).
- `GET /api/v1/artworks`: Get a list of all artworks for the explore page.
- `GET /api/v1/artworks/{id}`: Retrieve details for a single artwork.
- `PUT /api/v1/artworks/{id}`: Update an existing artwork's details.
- `DELETE /api/v1/artworks/{id}`: Remove an artwork.

## 📦 Submission Requirements

- [ ] **GitHub Repository**: A private or public repository containing the complete backend source code.
- [ ] **Postman Collection**: A comprehensive collection for easy API testing and verification.
- [ ] **Detailed README.md**: Clear documentation covering setup, environment variables, and API usage.

## 🔮 Future Scope

- **Social Features**:
  - `POST /api/v1/artworks/{id}/like`: Allow users to like an artwork.
  - `POST /api/v1/artworks/{id}/comment`: Enable commenting on artworks.
  - `POST /api/v1/users/{username}/follow`: Implement user-following functionality.
- **Advanced Search**: Implement powerful search and filtering for artworks and artists.

---

## 👨‍💻 Author

| Profile | Developer Name | Role | GitHub | LinkedIn | X |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [![Sami](https://github.com/saidulalimallick04.png?size=75)](https://github.com/saidulalimallick04) | Saidul Ali Mallick (Sami) | Backend Developer & AIML Engineer & Team Lead | [@saidulalimallick04](https://github.com/saidulalimallick04) | [@saidulalimallick04](https://linkedin.com/in/saidulalimallick04) | [@saidulmallick04](https://x.com/saidulmallick04) |

> ❤️ I believe in building impact, not just writing code.
> *💚 Backend Sage signing off..*
---
