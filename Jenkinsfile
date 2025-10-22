pipeline {
    agent any

    environment {
        APP_DIR = "/home/ec2-user/streamlit-app"
        PORT = "8501"
    }

    stages {
        stage('Setup') {
            steps {
                sh "mkdir -p ${APP_DIR}"
            }
        }

        stage('Pull Code') {
            steps {
                dir("${APP_DIR}") {
                    git branch: 'main', url: 'https://github.com/<your-repo>.git'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    python3 -m pip install --upgrade pip
                    pip3 install -r ${APP_DIR}/requirements.txt
                """
            }
        }

        stage('Run Streamlit App') {
            steps {
                sh """
                    fuser -k ${PORT}/tcp || true
                    nohup streamlit run ${APP_DIR}/app.py --server.port ${PORT} --server.address 0.0.0.0 > ${APP_DIR}/app.log 2>&1 &
                """
            }
        }
    }

    post {
        success {
            echo "✅ Streamlit app deployed successfully at http://<EC2_PUBLIC_IP>:${PORT}"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
