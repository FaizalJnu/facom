# Flask MongoDB CRUD API

This is a RESTful CRUD API built with Flask and MongoDB, containerized with Docker for easy setup and deployment. The application provides endpoints for managing user resources with complete Create, Read, Update, and Delete operations.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing the API with Postman](#testing-the-api-with-postman)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Docker
- Docker Compose
- Postman (for API testing)

### Installing Docker and Docker Compose

#### Ubuntu/Pop!_OS/Debian-based systems:
```bash
# Update package information
sudo apt update

# Install Docker
sudo apt install docker.io

# Install Docker Compose
sudo apt install docker-compose

# Start and enable the Docker service
sudo systemctl enable --now docker

# Add your user to the docker group to run Docker without sudo
sudo usermod -aG docker $USER

# Log out and log back in for the group changes to take effect
```

#### macOS:
1. Download and install Docker Desktop from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac/)
2. Docker Compose is included with Docker Desktop for macOS

#### Windows:
1. Download and install Docker Desktop from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
2. Docker Compose is included with Docker Desktop for Windows
3. Ensure WSL 2 is set up properly (Docker Desktop will guide you)

## Project Setup

1. Clone the repository or create a new directory for the project:
```bash
mkdir -p flask-mongodb-api
cd flask-mongodb-api
```

2. Create the project structure:
```bash
mkdir -p app/models app/routes app/utils
```

3. Copy all project files into the appropriate directories or create them according to the [Project Structure](#project-structure) section.

## Running the Application

1. From the project root directory (where `docker-compose.yml` is located), run:
```bash
docker-compose up --build
```

2. The application will be accessible at `http://localhost:5000`.

3. You should see logs indicating that both the Flask application and MongoDB are running:
```
flask-app_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
flask-app_1  |  * Restarting with stat
flask-app_1  |  * Debugger is active!
```

4. To stop the application, press `Ctrl+C` in the terminal where it's running, or run:
```bash
docker-compose down
```

## API Endpoints

The API provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | Get all users |
| GET | /users/{id} | Get a specific user by ID |
| POST | /users | Create a new user |
| PUT | /users/{id} | Update an existing user |
| DELETE | /users/{id} | Delete a user |
| GET | /health | Check API health status |

## Testing the API with Postman

### 1. Get All Users
- **Method**: GET
- **URL**: `http://localhost:5000/users`
- **Expected Response**: JSON array of users

### 2. Create a New User
- **Method**: POST
- **URL**: `http://localhost:5000/users`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123"
}
```
- **Expected Response**: Created user object with 201 status code

### 3. Get a Specific User
- **Method**: GET
- **URL**: `http://localhost:5000/users/{id}` (Replace `{id}` with an actual user ID)
- **Expected Response**: User object matching the specified ID

### 4. Update a User
- **Method**: PUT
- **URL**: `http://localhost:5000/users/{id}` (Replace `{id}` with an actual user ID)
- **Headers**: `Content-Type: application/json`
- **Body** (including only fields to update):
```json
{
    "name": "Updated Name",
    "email": "updated.email@example.com"
}
```
- **Expected Response**: Updated user object

### 5. Delete a User
- **Method**: DELETE
- **URL**: `http://localhost:5000/users/{id}` (Replace `{id}` with an actual user ID)
- **Expected Response**: Success message with 200 status code

### 6. Check API Health
- **Method**: GET
- **URL**: `http://localhost:5000/health`
- **Expected Response**: `{"status": "healthy"}`

## Project Structure

```
facom/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── config.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## Troubleshooting

### Common Issues:

1. **Port conflicts**:
   - If port 5000 or 27017 is already in use, you can modify the ports in `docker-compose.yml`.

2. **Connection issues**:
   - Ensure Docker services are running: `sudo systemctl status docker`
   - Check container status: `docker ps -a`

3. **Null ID issues**:
   - If users appear with null IDs, ensure MongoDB is correctly generating ObjectIDs.
   - Check the MongoDB connection in `app/__init__.py`.

4. **MongoDB Authentication**:
   - The default setup doesn't use authentication. For production, add MongoDB credentials.

5. **Application crashes**:
   - Check logs with `docker-compose logs flask-app`
   - If dependency errors occur, check `requirements.txt` for version conflicts.

### MongoDB Shell Access (for debugging):

```bash
# Access MongoDB shell from container
docker exec -it flask-mongodb-api_mongodb_1 mongosh

# Inside MongoDB shell
use user_db
db.users.find()  # List all users
```