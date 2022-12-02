pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cp -fr . /home/jenkins/loveletterwriter.api&&cd /home/jenkins/loveletterwriter.api&&git remote -v &&git pull origin update/dev&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
