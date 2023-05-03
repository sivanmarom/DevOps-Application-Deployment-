

pipeline {
    agent { label 'slave1' }
    environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
    VERSION = '1.0'
      }
    stages {
      stage('git clone') {
            steps {
                sh 'rm -rf project-flask-app'
                sh 'git clone https://github.com/sivanmarom/project-flask-app.git'
            }
        }
        stage('Build Docker image') {
           steps {
                sh 'sudo docker build -t flask_image:${VERSION} .'
               sh "sudo docker run -it --name flaskApp -p 5000:5000 -d flask_image:${VERSION}"
          }
    }
      stage('Testing') {
            steps {
                sh 'cd project-flask-app'
                sh 'pytest test-try.py::Test_class --html=report.html'
            }
        }

        stage("build user") {
  steps{
    wrap([$class: 'BuildUser', useGitAuthor: true]) {
      sh 'echo ${BUILD_USER} >> Result.json'
    }
  }
}
//       stage("testing") {
//     steps {
//         script {
//            STATUS = sh(script: "curl -I \$(dig +short myip.opendns.com @resolver1.opendns.com):5000 | grep \"HTTP/1.1 200 OK\" | tr -d \"\\r\\n\"", returnStdout: true).trim()
//             sh 'echo "$STATUS" >> Result.json'
//             sh 'echo "$TIME" >> Result.json'
//             withAWS(credentials: 'awscredentials', region: 'us-east-1') {
//                 sh "aws dynamodb put-item --table-name test-result --item '{\"user\": {\"S\": \"${BUILD_USER}\"}, \"date\": {\"S\": \"${TIME}\"}, \"state\": {\"S\": \"${STATUS}\"}}'"
//             }
//         }
//     }
//       }
//
        stage ('upload to s3 bucket'){
            steps{
                withAWS(credentials: 'aws-credentials'){
                     sh 'aws s3 cp report.html s3://test-result-flask-app'
                }
            }
        }

        stage('Parse Log File') {
    steps {
        script {
            def log_file_path = "${WORKSPACE}/project-flask-app/logfile.log"
            def log_entries = []
            def logger = logging.getLogger()
            def fh = new logging.FileHandler(log_file_path)
            def formatter = new logging.Formatter('%(asctime)s :%(levelname)s : %(message)s :')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.setLevel(logging.DEBUG)
            new File(log_file_path).eachLine { line ->
                def record = logger.makeRecord('record', logging.DEBUG, null, null, line, null, null)
                log_entries.add([
                    'timestamp': record.created,
                    'level': record.levelname,
                    'message': record.getMessage(),
                ])
            }
            println "Parsed log entries: ${log_entries}"
            env.LOG_ENTRIES = groovy.json.JsonOutput.toJson(log_entries)
        }
    }
}
        stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh 'sudo docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
            sh 'sudo docker tag flask_image:${VERSION} sivanmarom/test:flask_image'
            sh 'sudo docker push sivanmarom/test:flask_image'
        }
    }
}
// //
// //         stage('stop conatiner'){
// //             steps {
// //
// //                 sh' sudo docker stop flaskApp'
// //                 sh 'sudo docker rm flaskApp'
// //             }
// //         }
    }
    post {
        always {
            deleteDir()
        }
    }
}
