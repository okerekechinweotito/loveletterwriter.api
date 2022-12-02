pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {

sh "sudo rm -rf ./*"
sh "git pull origin update/dev"
sh "git config user.name 'idimmusix'"
sh "git config user.email 'idimmusix@gmail.com'"
checkout scm
                            sh "git switch update/dev&&git merge update/dev&&ls -a .&&cp -fr . /home/jenkins/loveletterwriter.api&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
