pipeline {
	agent any
	
	stages {

		stage("setup backend"){
			steps {
                            sh "cd /home/jenkins&&sudo git clone git@github.com:workshopapps/loveletterwriter.api&&cd loveletterwriter.api&&sudo cp -rn /home/idimmusix/loveletterwriter.api .&&sudo git config pull.ff only &&sudo git switch update/dev&&sudo git pull origin update/dev&&sudo chown -R jenkins:idimmusix .&&source env/bin/activate&&pip install --upgrade pip&&pip install -r 'requirements.txt'&&alembic revision --autogenerate -m '${env.BUILD_ID}'&&alembic upgrade head"     
                        }
		}
		stage("restart server"){
                       steps {
                        sh 'sudo systemctl restart hng'
                       }
                 }
    }
}
