pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cp -rn . /home/jenkins&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&source env/bin/activate&&pip3.11 install --upgrade pip&&pip3.11 install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
		
    }
}
