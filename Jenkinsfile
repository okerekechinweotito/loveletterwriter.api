pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "git branch&&git merge update/dev&&ls -a .&&git switch update/dev&&git branch&&cp -fr . /home/jenkins/loveletterwriter.api&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
