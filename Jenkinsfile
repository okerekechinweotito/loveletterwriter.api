pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cp -rf . /home/jenkins/loveletterwriter.api&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&source env/bin/activate&&pip install --upgrade pip&&pip install --no-cache-dir -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
		
    }
}
