pipeline{

    agent { label 'slave1' }
    environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
    VERSION_FILE = 'home/ubuntu/version.txt'
    VERSION = sh(script: "cat $VERSION_FILE", returnStdout: true).trim() ?: "1.0"


    }
    stages{
        stage('git clone') {
            steps {
                dir('/home/ubuntu/workspace/pipeline-try') {
                    sh 'rm -rf *'
                    sh 'git clone https://github.com/sivanmarom/project-flask-app.git'
                }
            }
        }
        stage('Build Docker image') {
           steps {
                dir('/home/ubuntu/workspace/pipeline-try/project-flask-app') {
                sh 'sudo docker build -t flask_image:${VERSION} .'
               sh "sudo docker run -it --name flaskApp -p 5000:5000 -d flask_image:${VERSION}"
          }
          }
        }
        stage('Testing') {
            steps {
                 dir('/home/ubuntu/workspace/pipeline-try/project-flask-app') {
                sh 'pytest test-try.py::Test_class --html=report.html'
            }
           }
        }
        stage("build user") {
    steps {
        wrap([$class: 'BuildUser', useGitAuthor: true]) {
            script {
                env.BUILD_USER = BUILD_USER
            }
        }
    }
}
        stage ('upload to s3 bucket'){
            steps{
            dir('/home/ubuntu/workspace/pipeline-try/project-flask-app') {
                withAWS(credentials: 'aws-credentials'){
                     sh 'aws s3 cp report.html s3://test-result-flask-app'
                }
                }
            }
        }
        stage('Upload to dynamodb') {
    steps {
        dir('/home/ubuntu/workspace/pipeline-try/project-flask-app') {
            script {
                def log_entry = sh(script: 'python3.8 parse_log_file.py', returnStdout: true).trim()
                def (timestamp, message) = log_entry.split(',')
                message = message.replaceAll('"', '\\"') // add this line to escape quotation marks
                withAWS(credentials: 'aws-credentials', region: 'us-east-1') {
                 sh "aws dynamodb put-item --table-name project-result --item \"{\\\"user\\\": {\\\"S\\\": \\\"${env.BUILD_USER}\\\"}, \\\"timestamp\\\": {\\\"S\\\": \\\"${timestamp}\\\"}, \\\"message\\\": {\\\"S\\\": \\\"${message}\\\"}}\""
                }
            }
        }
    }
}

        stage('Push to Docker Hub') {
        steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh 'sudo docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
            sh 'sudo docker tag flask_image:${VERSION} sivanmarom/test:flask_image-${VERSION}'
            sh 'sudo docker push sivanmarom/test:flask_image-${VERSION}'
            script{
                if (VERSION_FILE.exists()){
                def new_version = VERSION.toFloat() + 1
                VERSION_FILE.write(new_version)
                VERSION =new_version
                }
            }
            sh 'if [ $? -eq 0 ]; then VERSION=$(echo $VERSION+1 | bc); echo $VERSION > /home/ubuntu/version.txt; fi'
                }
            }
        }
    }
  post {
        always {
            deleteDir()
        }
    }
}