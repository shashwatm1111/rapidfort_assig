
# Doc-to-PDF App

This is a Dockerized web application that converts documents (e.g., DOC, DOCX) to PDF format. The app is deployed and accessible via a live link, and the Docker image is available for use.

- **Docker Image**: [Doc-to-PDF App Docker Image on Docker Hub](https://hub.docker.com/layers/shashwat543/doc-to-pdf-app/v2/images/sha256-8bb72aea3b11a440e8d4c9d1c23092f494c81dc4e9329c28dd3a6041c19b4863?context=repo)
- **Live Deployed App**: [Doc-to-PDF App](https://doc-to-pdf-app-v2.onrender.com/)

## Features

- Convert documents (DOC, DOCX) to PDF format.
- Dockerized application for easy deployment.
- Deployed on [Render](https://doc-to-pdf-app-v2.onrender.com/) for cloud access.
- Password protection for PDF files (allow users to set a password while converting documents to PDF).
- Kubernetes deployment support for scaling the application on cloud infrastructure.
  
## Technologies Used

- **Python**: The core programming language used for the backend logic of the application.
- **Flask**: A lightweight web framework used for building the web API that handles the document conversion process.
- **Docker**: Containerized the application to ensure consistency across different environments and for easier deployment.
- **Kubernetes**: Used for orchestrating the app in a cloud environment for high availability and scaling.
- **Render**: Deployed the application on Render for cloud hosting and access.
- **GitHub Actions**: Used to automate the build, test, and deployment pipeline of the Docker image to the cloud.

## Docker Image

This application is packaged in a Docker image, making it easy to deploy anywhere with Docker support.

### To Use the Docker Image

1. **Pull the Docker image**:
   ```bash
   docker pull shashwat543/doc-to-pdf-app:v2
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8080:8080 shashwat543/doc-to-pdf-app:v2
   ```

3. Visit `http://localhost:8080/` in your browser to interact with the app.

## Deploying to Your Own Server

You can deploy this app to your own cloud server using Docker. Here’s how:

1. **Install Docker** on your server.
   - For Ubuntu, you can follow [this guide](https://docs.docker.com/engine/install/ubuntu/).

2. **Pull the Docker image**:
   ```bash
   docker pull shashwat543/doc-to-pdf-app:v2
   ```

3. **Run the application**:
   ```bash
   docker run -d -p 80:8080 shashwat543/doc-to-pdf-app:v2
   ```

4. Your server will now host the app, accessible via `http://your-server-ip/`.

### How to Run the Application

1. Clone the repository.
2. Navigate to the project directory.
3. Run the `run.sh` script to start the application.

## API Endpoints

The app provides a simple web interface for document conversion. Upload your document via the UI to convert it into PDF. The backend API is available as follows:

- **POST `/upload`**: Upload a document to be converted to PDF.

## Continuous Deployment with GitHub Actions

This project is integrated with GitHub Actions to automatically build and deploy the Docker image to the cloud. Every time a change is pushed to the `main` branch, the application is rebuilt and deployed.

### GitHub Actions Workflow

Here’s the basic workflow setup for GitHub Actions:

1. **Build Docker Image**: Every push to the repository triggers a Docker image build.
2. **Deploy to Server**: The image is pushed to Docker Hub and automatically deployed to a server.


