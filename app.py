import subprocess

import jenkins
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from paramiko import file

import iam_user_creation
import launch_instance

app = Flask(__name__)
my_users = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __str__(self):
        return f"Username: {self.user_name}, password:{self.password}"


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        my_users.append(user_name)
        p = Profile(user_name=user_name, password=password)
        db.session.add(p)
        db.session.commit()
        return redirect("/homepage")
    return render_template("signup.html")


@app.route('/docker', methods=['POST', 'GET'])
def docker():
    if request.method == 'POST':
        image_name = request.form.get('image_name')
        subprocess.run(['docker', 'build', '-t', f'{image_name}', '.'])
        subprocess.run(['docker', 'tag', f'{image_name}', f'sivanmarom/test:{image_name}'])
        subprocess.run(['docker', 'login', '-u', 'sivanmarom', '-p', 'sm5670589'])
        subprocess.run(['docker', 'push', f'sivanmarom/test:{image_name}'])
        return f'Docker image {image_name} created and pushed to Docker Hub'
    else:
        return render_template('docker.html')


@app.route('/homepage')
def homepage():
    return render_template("homepage.html", my_users=my_users)


@app.route('/aws', methods=['POST', 'GET'])
def create_and_launch():
    if request.method == 'POST':
        if request.form['submit'] == 'Create user':
            user_name = request.form.get('username')
            password = request.form.get('password')
            access_keys = iam_user_creation.create_iam_user_and_access_key(user_name=user_name, password=password)
            access_key_id = access_keys["AccessKey"]["AccessKeyId"]
            secret_access_key = access_keys["AccessKey"]["SecretAccessKey"]
            return redirect(
                url_for('result', user_name=user_name, password=password, access_key_id=access_key_id,
                        secret_access_key=secret_access_key))
        elif request.form['submit'] == 'Create instance':
            instance_name = request.form.get('instance_name')
            instance_type = request.form.get('instance_type')
            key_pair_name = request.form.get('key_pair_name')
            image_id = request.form.get('image_id')
            security_group_id = request.form.get('security_group_id')
            instance_count = int(request.form['instance_count'])
            add_docker = 'add_docker' in request.form
            add_jenkins ='add_jenkins' in request.form
            i = 1
            while i <= instance_count:
                public_ip=launch_instance.launch_ec2_instance(instance_name=instance_name, instance_type=instance_type,
                                                    key_pair_name=key_pair_name, image_id=image_id,
                                                    security_group_id=security_group_id, instance_count=1, add_docker=add_docker, add_jenkins=add_jenkins)
                i += 1

            print(public_ip)
            return redirect('/launched')
    return render_template("aws.html")


@app.route('/iam_creation_user_result')
def result():
    return render_template('iam_creation_user_result.html',
                           user_name=request.args.get('user_name'),
                           password=request.args.get('password'),
                           access_key_id=request.args.get('access_key_id'),
                           secret_access_key=request.args.get('secret_access_key'))

@app.route('/create_jenkins_job', methods=['POST', 'GET'])
def create_jenkins_job():
    if request.form == "POST":
        job_name = request.form.get("job_test")
        server = jenkins.Jenkins('http://3.95.221.78:8080', username='admin', password='admin')
        with open('templates/jenkins_job.xml', 'r') as f:
            job_config_xml = f.read()
        server.create_job(job_name, job_config_xml)
        return "job created successfully"
    return render_template('create_jenkins_job.html')


@app.route('/launched')
def launched():
    return render_template("launched.html")


@app.route('/jenkins', methods=['POST', 'GET'])
def create_jenkins_user():
    # server = jenkins.Jenkins(f'http://{public_ip}:8080', username='your-jenkins-username',
    #                          password='your-jenkins-api-token')
    #
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     full_name = request.form.get('full_name')
    #     email = request.form.get('email')
    #     new_user = {
    #         username: username,
    #         password: password,
    #         full_name: full_name,
    #         email: email
    #     }
    return render_template('jenkins.html')

if __name__ == "__main__":
    app.run(debug=True)
