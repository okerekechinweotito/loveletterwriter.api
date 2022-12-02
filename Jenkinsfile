pipeline {
	agent any
	
	stages {

		stage("setup backend"){

			steps {
                                sh 'sudo ls /home/idimmusix/&&sudo cp -rn /home/idimmusix/loveletterwriter.api/* .&&./env/bin/activate&&pip install -r "requirements.txt"&&alembic revision --autogenerate -m "${env.BUILD_ID}"&&alembic upgrade head'
                                sh 'sudo cp -rn . /home/idimmusix/loveletterwriter.api'
                }
			}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systmctl restart hng'
                       }
                 }
		
    }
}
