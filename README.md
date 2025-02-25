Below is an updated example README that includes instructions for both deploying your Flask app on AWS Elastic Beanstalk and on a VPS (such as with IONOS web hosting).

* * *

Flask AI Assistant Deployment
=============================

This repository contains a simple Flask-based AI assistant that uses Elasticsearch and OpenAI to answer questions. This guide explains how to set up your development environment, run the Flask app locally, and deploy the application either on AWS Elastic Beanstalk or on a VPS (e.g., IONOS web hosting).

* * *

Table of Contents
-----------------

*   [Prerequisites](#prerequisites)
*   [Project Structure](#project-structure)
*   [Local Setup](#local-setup)
    *   [1\. Clone the Repository](#1-clone-the-repository)
    *   [2\. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
    *   [3\. Install Dependencies](#3-install-dependencies)
    *   [4\. Configure Environment Variables](#4-configure-environment-variables)
    *   [5\. Run the App Locally](#5-run-the-app-locally)
*   [Deployment to AWS Elastic Beanstalk](#deployment-to-aws-elastic-beanstalk)
    *   [1\. Install and Configure the EB CLI](#1-install-and-configure-the-eb-cli)
    *   [2\. Create the Application and Environment](#2-create-the-application-and-environment)
    *   [3\. Prepare the Deployment Package](#3-prepare-the-deployment-package)
    *   [4\. Deploy the Application](#4-deploy-the-application)
*   [Deployment to VPS with IONOS Web Hosting](#deployment-to-vps-with-ionos-web-hosting)
    *   [1\. Prepare Your VPS](#1-prepare-your-vps)
    *   [2\. Upload Your Application Code](#2-upload-your-application-code)
    *   [3\. Set Up the Virtual Environment and Install Dependencies](#3-set-up-the-virtual-environment-and-install-dependencies)
    *   [4\. Configure a Production Server (Gunicorn & NGINX)](#4-configure-a-production-server-gunicorn--nginx)
    *   [5\. Start and Manage Your Application](#5-start-and-manage-your-application)
*   [Custom Domain and HTTPS (Optional)](#custom-domain-and-https-optional)
*   [Troubleshooting](#troubleshooting)
*   [License](#license)

* * *

Prerequisites
-------------

*   **Python 3.8 or 3.9** installed on your local machine.
*   For AWS Elastic Beanstalk:
    *   **AWS CLI** and **EB CLI** installed and configured.
    *   An AWS account with permissions to create Elastic Beanstalk applications.
*   For VPS deployment (IONOS):
    *   A VPS running a supported Linux distribution (e.g., Ubuntu, CentOS).
    *   SSH access to your VPS.
    *   Root or sudo privileges.
*   A valid SSL certificate if you plan to use HTTPS (optional).

* * *

Project Structure
-----------------

```
.
├── .ebextensions
│   └── 01_install.config       # Container commands for EB dependency installation
├── .env                        # Environment variables (not checked into Git)
├── .ebignore                   # Files/folders to exclude from EB deployment
├── Procfile                    # Gunicorn command for EB deployment
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── rotary_ai.py                # Main Flask application code
└── wsgi.py                     # WSGI entry point for Gunicorn
``` 

* * *

Local Setup
-----------

### 1\. Clone the Repository

`git clone https://github.com/poulsbopete/rotary_ai_assistant.git
cd rotary_ai_assistant` 

### 2\. Create and Activate a Virtual Environment

`python3 -m venv myenv
source myenv/bin/activate   # On Windows: myenv\Scripts\activate` 

### 3\. Install Dependencies

`pip install --upgrade pip setuptools wheel
pip install -r requirements.txt` 

_Your `requirements.txt` should include dependencies like Flask, Flask-Cors, Elasticsearch, OpenAI, etc._

### 4\. Configure Environment Variables

Create a `.env` file in the project root and add:

`ES_API_KEY=your_elasticsearch_api_key
OPENAI_API_KEY=your_openai_api_key` 

These variables will be loaded using `python-dotenv`.

### 5\. Run the App Locally

Run the app using the WSGI entry point:

`python wsgi.py` 

Visit `http://127.0.0.1:8000` in your browser to test the application.

* * *

Deployment to AWS Elastic Beanstalk
-----------------------------------

### 1\. Install and Configure the EB CLI

Install the EB CLI if you haven’t:

`pip install awsebcli --upgrade --user` 

Configure your AWS credentials:

`aws configure` 

Then initialize Elastic Beanstalk for your project:

`eb init` 

Follow the prompts:

*   Choose your AWS region (e.g., `us-west-2`).
*   Select your application name (e.g., `my-python-app`).
*   Choose the appropriate Python platform (e.g., "Python 3.9 running on 64bit Amazon Linux 2").

### 2\. Create the Application and Environment

Create a new environment:

`eb create rotary-python-env --platform "Python 3.9 running on 64bit Amazon Linux 2"` 

If you encounter platform issues, run:

`eb platform list` 

to see available options.

### 3\. Prepare the Deployment Package

*   **Exclude Local Virtual Environment:**  
    Create a `.ebignore` file in your project root:
    
    bash
    
    `myenv/
    *.pyc
    __pycache__/
    .git/
    .env` 
    

### 4\. Deploy the Application

Deploy using:

`eb deploy` 

Monitor the logs with:

`eb logs` 

* * *

Deployment to VPS with IONOS Web Hosting
----------------------------------------

### 1\. Prepare Your VPS

*   **Set Up Your VPS:**  
    Ensure your VPS (e.g., from IONOS) is running a supported Linux distribution.
*   **Update the System:**
    
    `sudo apt update && sudo apt upgrade -y   # For Debian/Ubuntu systems` 
    
*   **Install Python and pip:**
    
    `sudo apt install python3 python3-venv python3-pip -y` 
    

### 2\. Upload Your Application Code

*   **Using Git:**  
    Clone your repository on your VPS:
    
    `git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name` 
    
*   **Or via SFTP/FTP:**  
    Use an SFTP client to upload your project files.

### 3\. Set Up the Virtual Environment and Install Dependencies

Create and activate a virtual environment on your VPS:

`python3 -m venv myenv
source myenv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt` 

### 4\. Configure a Production Server (Gunicorn & NGINX)

*   **Gunicorn:**  
    Create a Gunicorn systemd service file (e.g., `/etc/systemd/system/myapp.service`):
    
    `[Unit]
    Description=Gunicorn instance to serve Flask AI Assistant
    After=network.target
    
    [Service]
    User=your_username
    Group=www-data
    WorkingDirectory=/path/to/your/project
    Environment="PATH=/path/to/your/project/myenv/bin"
    ExecStart=/path/to/your/project/myenv/bin/gunicorn -w 3 -b 0.0.0.0:8000 wsgi:application
    
    [Install]
    WantedBy=multi-user.target` 
    
    Then, reload systemd and start your service:
    
    `sudo systemctl daemon-reload
    sudo systemctl start myapp.service
    sudo systemctl enable myapp.service` 
    
*   **NGINX:**  
    Install and configure NGINX as a reverse proxy:
    
    `sudo apt install nginx -y` 
    
    Create a new NGINX config file (e.g., `/etc/nginx/sites-available/myapp`):
    
    `server {
        listen 80;
        server_name yourdomain.com;  # Update with your domain or VPS IP
    
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }` 
    
    Enable the configuration and restart NGINX:
    
    `sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx` 
    

### 5\. Start and Manage Your Application

*   **Check the status of your Gunicorn service:**
    
    `sudo systemctl status myapp.service` 
    
*   **View application logs** (if configured in systemd or via Gunicorn logs).

* * *

Custom Domain and HTTPS (Optional)
----------------------------------

*   **Custom Domain:**  
    Update your DNS records (e.g., via IONOS) to point your domain to your VPS’s IP address.
*   **HTTPS:**  
    Use Let’s Encrypt to obtain a free SSL certificate:
    
    `sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d yourdomain.com` 
    
    Follow the prompts to configure HTTPS and auto-renewal.

* * *

Troubleshooting
---------------

*   **502 Bad Gateway on Elastic Beanstalk or VPS:**  
    Check your logs (via `eb logs` on AWS or NGINX/Gunicorn logs on VPS) for errors.
*   **Dependency Issues:**  
    Ensure your `requirements.txt` is up-to-date and that your virtual environment is activated.
*   **Method Not Allowed:**  
    Ensure your endpoints are using the correct HTTP methods.

* * *

License
-------

This project is licensed under the MIT License.

* * *

This README provides a comprehensive guide for both AWS Elastic Beanstalk and IONOS VPS deployments. Adjust any paths, domain names, or configuration details as needed for your setup. Let me know if you need further clarification or additional instructions!
