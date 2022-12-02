pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "sudo add-apt-repository ppa:deadsnakes/ppa&&sudo apt update&&sudo apt install python3.11&&cp -rn . /home/jenkins&&cd /home/jenkins/loveletterwriter.api&&git switch update/dev&&python3.10 -m venv env&&source env/bin/activate&&pip3.11 install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
		
    }
}
