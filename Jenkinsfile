pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "ls ${WORKSPACE}"
                            sh "cd /home/jenkins/loveletterwriter.api &&sudo chown -R root:root .&&sudo git switch update/dev&&sudo git pull origin update/dev&&sudo chown -R jenkins:idimmusix /home/jenkins&&python3.11 -m venv env&&source env/bin/activate&&pip install --upgrade pip&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                        sh 'sudo systemctl restart celery'
                        sh 'sudo systemctl restart celerybeat'
                       }
                 }
        }
        post {
        failure {
            emailext attachLog: true, 
            to: 'contact.lovemeapp@gmail.com, idimmusix@gmail.com',
            subject: '${BUILD_TAG} Build failed',
            body: '${BUILD_TAG} Build Failed \nMore Info can be found here: ${BUILD_URL} or in the log file below'
        }
    }
}
