pipeline {
	agent any
	
	stages {

		stage("setup backend"){

			steps {
                                sh 'cd /home/idimmusix/loveletterwriter.api&&git pull https://github.com/workshopapps/loveletterwriter.api&&source env/bin/activate&&pip install -r "requirements.txt"&&alembic revision --autogenerate -m "${env.BUILD_ID}"&&alembic upgrade head'
                }
			}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systmctl restart hng'
                       }
                 }
		
    }
}
