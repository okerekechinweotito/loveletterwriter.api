pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            
                            sh "cd /home/jenkins/loveletterwriter.api &&sudo chown -R root:root .&&sudo git switch update/dev&&sudo git pull origin update/dev&&sudo chown -R jenkins:idimmusix /home/jenkins&&python3.11 -m venv env&&source env/bin/activate&&pip install --upgrade pip&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&mkdir alembic/versions&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
