# Fullstack Training Developer Document

## Project Purpose

This training project is designed to help students understand:

- How to interact with backend APIs from a frontend application.
- How frontend and backend communicate using clearly defined interfaces.
- How a basic fullstack CRUD system works, covering:
  - User registration
  - User login
  - Profile update
  - File upload

## Technology Stack

**Frontend:** HTML, CSS, JavaScript (optional: React)  
**Backend:** FastAPI (Python)

## Shared Interfaces

These interfaces define the structure of data that both the frontend and backend must agree on.

### Authentication

#### Register (POST `/api/auth/register`)

**Request:**

```ts
interface RegisterDTO {
  name: string;
  email: string;
  password: string;
}
```

**Response:**

```ts
interface AuthResponse {
  message: string;
  user: {
    id: string;
    name: string;
    email: string;
  };
  token: string;
}
```

#### Login (POST `/api/auth/login`)

**Request:**

```ts
interface LoginDTO {
  email: string;
  password: string;
}
```

**Response:**
Same as `AuthResponse`

### Profile

#### Get Profile (GET `/api/user/profile`)

**Headers:**

```
Authorization: Bearer <token>
```

**Response:**

```ts
interface UserProfile {
  id: string;
  name: string;
  email: string;
  profilePictureUrl?: string;
}
```

#### Update Profile (PUT `/api/user/profile`)

**Request:**

```ts
interface UpdateUserDTO {
  name?: string;
  email?: string;
}
```

**Response:**

```ts
interface UpdateResponse {
  message: string;
  updatedUser: UserProfile;
}
```

### Upload Profile Picture (POST `/api/user/upload`)

**Request:** multipart/form-data with a `file` field.

**Response:**

```ts
interface UploadResponse {
  message: string;
  profilePictureUrl: string;
}
```

## Common API Response Wrapper

All API responses should use the following wrapper:

```ts
interface ApiResponse<T> {
  status: "success" | "error";
  message: string;
  data?: T;
}
```

## Development Agreement

- Shared types/interfaces must be documented and strictly followed.
- FastAPI Swagger docs will be used to verify endpoint contracts.
