pipeline {
	agent any
	
	stages {

		stage("setup backend"){

			steps {
				
                                sh '''#!/bin/bash
                                      sudo cp -rn /home/idimmusix/loveletterwriter.api/env .
                                      sudo cp -r /home/idimmusix/loveletterwriter.api/alembic .
                                      sudo cp /home/idimmusix/loveletterwriter.api/.env . 
                                      source env/bin/activate&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head'''
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
