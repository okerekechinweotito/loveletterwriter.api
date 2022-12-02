pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cd /home/jenkins/loveletterwriter.api&&git remote -v &sudo git pull git@github.com:workshopapps/loveletterwriter.api&&sudo git switch update/dev&&sudo chown -R jenkins:idimmusix .&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
