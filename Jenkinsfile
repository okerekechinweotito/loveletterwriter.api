pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "sudo apt install python3.11 -y&&cp -rn . /home/jenkins&&sudo apt install python3.11-venv&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&python3.11 -m venv env&&source env/bin/activate&&pip3.11 install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
		
    }
}
