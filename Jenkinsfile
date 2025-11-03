pipeline {
    agent any
    environment {
        API_KEY = credentials('AZURE_OPENAI_API_KEY')
        DEPLOYMENT_NAME = credentials('AZURE_OPENAI_DEPLOYMENT')
        HUGGINGFACE_API_KEY = credentials('HUGGINGFACE_API_KEY')
        DOCKER_IMAGE = 'heena1707/gamepulse:v2'
        CONTAINER_NAME = 'genai-gamepulse-app'
        EC2_USER = 'ec2-user'
        EC2_HOST = '34.226.211.27'
        EC2_KEY_SECRET = 'ec2-ssh' // Your Jenkins secret ID storing PEM content
    }
    stages {
        stage('Deploy on EC2') {
            steps {
                powershell """
                echo 'Writing PEM key to temp file...'
                \$keyPath = "C:\\\\ProgramData\\\\Jenkins\\\\ec2_key.pem"
                Set-Content -Path \$keyPath -Value \$env:EC2_KEY_SECRET
                icacls \$keyPath /inheritance:r /grant:r "%username%:R"
                
                echo 'Starting EC2 deployment...'
                ssh -i \$keyPath -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST `
                    "docker pull $DOCKER_IMAGE; `
                     docker rm -f $CONTAINER_NAME || true; `
                     docker run -d --name $CONTAINER_NAME -p 8501:8501 `
                        -e AZURE_OPENAI_API_KEY=$API_KEY `
                        -e AZURE_OPENAI_ENDPOINT=https://aoi-rotopoc-001.openai.azure.com/ `
                        -e AZURE_OPENAI_DEPLOYMENT=$DEPLOYMENT_NAME `
                        -e AZURE_OPENAI_API_VERSION=2024-05-01-preview `
                        -e HUGGINGFACE_API_KEY=$HUGGINGFACE_API_KEY $DOCKER_IMAGE"
                
                echo 'Deployment finished!'
                Remove-Item \$keyPath
                """
            }
        }
    }
}
