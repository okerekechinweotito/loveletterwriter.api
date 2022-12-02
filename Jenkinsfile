pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cp -fr . /home/jenkins/loveletterwriter.api&&cd /home/jenkins/loveletterwriter.api&&curl -u idimmusix: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 https://api.github.com/jenkins &&git pull https://github.com/workshopapps/loveletterwriter.api&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
