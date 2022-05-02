String cron_string = BRANCH_NAME == "master" ? "@daily" : ""

pipeline {
    agent any
    triggers { cron(cron_string) }
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Starting code checkout stage.'
                sh '''
                    #!/bin/sh
                    rm -rf
                '''
                git credentialsId: '9c7b1401-74d1-41ea-aa36-b2c440fd4485', url: 'https://github.com/cmu-seai/group-project-s22-furious-five.git'
                echo 'Code checked out successfully.'
            } // steps
        } // stage

        stage('Install Dependencies') {
           steps {
               echo 'Installing dependencies'
                sh '''
                    #!/bin/sh
                    pip3 install -r old_requirements.txt
                    pip3 install "fastapi[all]"
                '''
           }
        }

        stage('Evaluate Code Quality') {
           steps {
            	echo 'Run tests'
                sh '''
                    #!/bin/sh
                    python3 -m pytest --cov=./ --cov-report=xml ./
                '''
                cobertura coberturaReportFile: 'coverage.xml'
                echo 'Code quality check completed.'
            } // steps
        } // stage


       stage('Data Separation') {
           steps {
               echo 'Starting data seperation for training.'
               sh '''
                   python3 ./deployment/DataSeparator.py
                   
               '''
               echo 'Data Seperation completed.'
           } // steps
       } // stage

       stage('Train Model') {
           steps {
               echo 'Start model training'
                sh '''
                    python3 ./deployment/trainModel.py 
                '''
               echo 'Model training completed.'
           } // steps
       }

        stage("Offline Evaluation") {
             steps {
                echo 'Start collecting telemetry data '
                sh '''
                    python3 ./deployment/OfflineEvaluation.py 
                '''
                echo 'Offline Evaluation Complete.'     

            } // steps
        } 

    } // stages
}
