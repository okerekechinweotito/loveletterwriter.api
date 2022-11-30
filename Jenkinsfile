pipeline {
        agent none
	
	stages {
		stage("setup python"){
                        agent any
                        steps {
                            dir(/home/idimmusix/loveletterwriter.api){
                                checkout scm
                                sh 'source env/bin/activate'
                                sh 'pip install -r "requirements.txt"'
                                sh 'alembic revision --autogenerate -m "${env.BUILD_ID}"'
                                sh 'alembic upgrade head'
                            } 
                        }                
                 }
                 stage("restart server"){
                      agent any
                       steps {
                        sh 'sudo systmctl restart hng'
                       }
                 }
		
        }
}
