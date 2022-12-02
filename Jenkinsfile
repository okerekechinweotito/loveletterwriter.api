pipeline {
	agent any
	
	stages {

		stage("setup backend"){

			steps {
                                sh 'sudo cd /var/www/loveme/loveletterwriter.api&&sudo git pull git@github.com:workshopapps/loveletterwriter.api&&sudo source env/bin/activate&&pip install -r "requirements.txt"&&alembic revision --autogenerate -m "${env.BUILD_ID}"&&alembic upgrade head'
                }
			}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systmctl restart hng'
                       }
                 }
		
    }
}
