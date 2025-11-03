pipeline {
agent any
environment {

    API_KEY = credentials('AZURE_OPENAI_API_KEY')
    DEPLOYMENT_NAME = credentials('AZURE_OPENAI_DEPLOYMENT')
    HUGGINGFACE_API_KEY = credentials('HUGGINGFACE_API_KEY')
    // Docker and container settings
    DOCKER_IMAGE = 'heena1707/gamepulse:v2'
    CONTAINER_NAME = 'genai-gamepulse-app'
    EC2_USER = 'ec2-user'
    EC2_HOST = '34.226.211.27'  // replace with your EC2 public IP
}
stages {
    stage('Deploy on EC2') {
        steps {
            sshagent(['ec2-ssh']) {  // Jenkins SSH credentials ID
                sh """
                ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST '
                    echo "Pulling latest Docker image..."
                    docker pull $DOCKER_IMAGE
                    
                    echo "Stopping and removing old container if exists..."
                    docker rm -f $CONTAINER_NAME || true
                    
                    echo "Running new container with environment variables..."
                    docker run -d \\
                        --name $CONTAINER_NAME \\
                        -p 8501:8501 \\
                          -e AZURE_OPENAI_API_KEY=$API_KEY \\
                          -e AZURE_OPENAI_ENDPOINT=https://aoi-rotopoc-001.openai.azure.com/ \\
                          -e AZURE_OPENAI_DEPLOYMENT=$DEPLOYMENT_NAME \\
                          -e AZURE_OPENAI_API_VERSION=2024-05-01-preview \\
                          -e HUGGINGFACE_API_KEY=$HUGGINGFACE_API_KEY \\
                        $DOCKER_IMAGE
                    
                    echo "Deployment complete!"
                '
                """
            }
        }
    }
}
}
