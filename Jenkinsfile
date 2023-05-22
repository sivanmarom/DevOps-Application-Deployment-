pipeline{

    agent { label 'slave1' }
    environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
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
                 withEnv(["VERSION=${env.VERSION}"]) {
                sh 'sudo docker build -t flask_image:${VERSION} .'
               sh "sudo docker run -it --name flaskApp -p 5000:5000 -d flask_image:${VERSION}"
               }
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
                }
            }
        }
        stage('Update Version') {
    steps {
        script {
            def newVersion = env.VERSION + 1
            sh "sudo sed -i 's/VERSION=.*/VERSION=${newVersion}/' /etc/environment"
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