pipeline {
	agent any
	
	stages {

		stage("setup backend"){

			steps {
                                sh 'sudo ls /home/idimmusix/&&sudo cp -rf /home/idimmusix/loveletterwriter.api/ . &&git pull&&source env/bin/activate&&pip install -r "requirements.txt"&&alembic revision --autogenerate -m "${env.BUILD_ID}"&&alembic upgrade head'
                                sh 'sudo cp -rf . /home/idimmusix/loveletterwriter.api'
                }
			}
		stage("restart server"){
            
                       steps {
                        sh 'sudo systmctl restart hng'
                       }
                 }
		
    }
}
