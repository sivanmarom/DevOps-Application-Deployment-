# DevOps Application Deployment 
This project focuses on the deployment and management of two applications using AWS resources, Jenkins, and automation tools. The first application involves controlling and managing AWS resources, Jenkins, and Docker Hub, while the second application retrieves user names and stores them in a database, providing a personalized greeting.

## Project Overview
The DevOps Application Deployment Project aims to automate the deployment and management of the applications through the following key components:

1. AWS Resources, Jenkins, and Docker Hub Integration: Provision and manage AWS resources using automation tools, integrate them with Jenkins for automated deployment, and control Docker Hub for image management.
2. Application 1: Control and Management App

&#8226; Description: An application that provides control and management functionalities for AWS resources and Docker Hub using various technologies.

&#8226; Technologies: AWS, Jenkins, Docker, Docker Hub

3. Application 2: User Retrieval and Greeting App

&#8226; Description: An application that retrieves user names during the sign-in process, stores them in a database, and greets the users.

&#8226; Technologies: Python, DynamoDB, Selenium, S3, Docker

4. Jenkins Pipeline:

&#8226; Description: A Jenkins pipeline that runs automated tests on the User Retrieval and Greeting App using Selenium.

&#8226; Technologies: Jenkins, Selenium, S3, DynamoDB, Docker

## Deployment and Lifecycle Management
The deployment and lifecycle management of the applications are orchestrated using Jenkins pipeline jobs. The Jenkins pipeline includes the following stages:

1. Build and Deployment: Triggers the deployment of the applications using Docker containers and manages the images on Docker Hub.

2. Testing and Reporting: Runs automated tests on the User Retrieval and Greeting App using Selenium, generates a test report, and uploads it to an S3 bucket. Logs are also stored in a DynamoDB table.

3. Production Deployment: If the tests pass successfully, the Docker image of the application is pushed to Docker Hub, triggering another job to deploy the image to production instances.

## AWS Setup
To successfully deploy the applications, follow these preliminary steps:

1. Create an AWS account and generate access credentials with appropriate permissions.
2. Install and configure the AWS CLI on your local machine.
3. Set up your AWS credentials locally by running aws configure and providing your access key and secret key.

## Repository Structure
The project repository is structured as follows:

&#8226; control-management-app/: Contains the source code and configuration files for the Control and Management App.

&#8226; user-retrieval-app/: Contains the source code and configuration files for the User Retrieval and Greeting App.

&#8226; jenkins-pipeline/: Includes the Jenkinsfile defining the pipeline stages and configurations.

&#8226; README.md: Project documentation providing an overview, instructions, and guidelines.

## Instructions
To successfully deploy and manage the applications, follow these steps:

1. Clone the project repository to your local machine.
2. Set up Jenkins with the required plugins and configurations.
3. Review and update the application-specific configuration files based on your specific requirements.
4. Customize the Jenkins pipeline stages and configurations in the jenkins-pipeline/ directory if necessary.
5. Execute the Jenkins pipeline job(s) to deploy and manage the applications.
6. Monitor the test results, generated reports, and logs stored in the S3 bucket and DynamoDB table.
7. If the tests pass, the application image will be pushed to Docker Hub, triggering the deployment to production instances.
8. Refer to the application-specific documentation and Jenkins pipeline job(s) for detailed instructions and usage guidelines.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: git checkout -b new-feature.
3. Make your changes and commit them: git commit -m 'Add some feature'.
4. Push your changes to the branch: git push origin new-feature.
5. Submit a pull request detailing your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
If you have any questions, suggestions, or feedback, please feel free to contact Sivan Marom at sivmarom@gmail.com.
