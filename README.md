<p align="center">
  <a href="" rel="noopener">
</p>

<h1 align="center">CloudPass</h1>

<div align="center">

</div>

---
<h3 align="center">
      This project demonstrates the use of my development skills to create a backend API that enables secure communication across multiple platforms. It incorporates industry-standard practices and production-level tactics, ensuring its readiness for deployment on an industry-wide scale. Leveraging Docker, the project follows industry-level standards for containerization, making it easily deployable on a server for seamless deployment and scalability.
      <br>
  </p>
  </h3>
  
## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>
      CloudPass is a highly secure cloud-based password manager that provides robust storage and management of user passwords. It consists of a backend API developed using FastAPI, incorporating industry-standard security measures such as JWT tokens for API security and hashed keys for storing user passwords. The database backend utilizes MariaDB for secure data storage. The website is built with Flask and is reverse proxied with NGINX. The entire application is containerized using Docker for easy deployment, scalability, and enhanced security.
## 🏁 Getting Started <a name = "getting_started"></a>
All you will need to get started is an updated version of Docker on any system

### Prerequisites
- Docker

### Running
The Cloud Password Manager can be deployed to any environment that supports Docker. By utilizing Docker containers, the deployment process becomes simplified and consistent across different platforms. Follow these steps for deployment:

- Set up a server or cloud instance with Docker installed.
- Clone the project repository to the server.
- Build and start the Docker containers using the provided Docker Compose file.

```
docker-compose build
docker-compose up -d
```


## 🎈 Usage <a name="usage"></a>
Once the Cloud Password Manager is up and running, users can perform the following actions:

- Register a new account with a unique username and password.
- Log in using the registered credentials, generating a secure JWT token for API authentication.
- Access and manage passwords securely through the user-friendly web interface.
- Generate strong passwords using customizable options for enhanced security.
- Analyze password strength to guide users towards creating robust passwords.
- Retrieve and update stored passwords while maintaining strict access control.
- Update account information and manage security settings.


## 🚀 Deployment <a name = "deployment"></a>
If you want to install this on a VPS it will be the same as described above just make sure you have the correct ports open and change the IP address in the settings found at the top of the rshell.py script.

## ⛏️ Built Using <a name = "built_using"></a>
- [Python3](https://www.python.org/) - Api and Website
- [MariaDB](https://mariadb.org/) - Database
- [NGINX](https://www.nginx.com/) - Reverse Proxy
- [Docker](https://www.docker.com/) - Containerization

## ✍️ Authors <a name = "authors"></a>
- [@brandongillett](https://github.com/brandongillett) - Developer

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- [@The-Documentation-Compendium](https://github.com/kylelobo/The-Documentation-Compendium) - Documentation behind the README
