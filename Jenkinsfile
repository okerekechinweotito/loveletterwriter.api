pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cd /home/jenkins/loveletterwriter.api&&sudo chown -R root:root /home/jenkins&&sudo python3.11 -m venv env&&sudo git switch update/dev&&sudo git pull origin update/dev&&source env/bin/activate&&pip install --upgrade pip&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
