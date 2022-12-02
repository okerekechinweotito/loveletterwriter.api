pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cp -rf . /home/jenkins&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&source env/bin/activate&&python3.11 -m pip install --upgrade pip&&python3.11 -m pip install --no-cache-dir -r 'requirements.txt'&&python3.11 -m alembic revision --autogenerate -m '${env.BUILD_ID}'&&python3.11 -m alembic upgrade head"     
                        }
		}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
		
    }
}
