// LAB 1: Docker integration + quality gate + smoke test
def deploy(String name, int port, String image, boolean bad) {
    def version = image.tokenize(':')[1]
    sh "docker rm -f ${name} || true"
    sh "docker run -d --name ${name} --network shopease-net -p ${port}:5000 --memory 256m --cap-drop ALL --security-opt no-new-privileges -e APP_VERSION=${version} -e BREAK_HEALTH=${bad} ${image}"
}

def smoke(String host) {
    withEnv(["HOST=${host}"]) {
        sh '''
            for i in 1 2 3 4 5 6 7 8 9 10; do
                curl -fsS http://$HOST:5000/health && echo && exit 0
                echo "waiting for $HOST ($i/10)..."; sleep 3
            done
            echo "health check FAILED for $HOST"; exit 1
        '''
    }
}

pipeline {
    agent any

    environment {
        IMAGE = "shopease/order-service:${BUILD_NUMBER}"
    }

    stages {
        stage('Quality Gate') {
            steps { sh 'docker build --progress=plain --target test .' }
        }
        stage('Build Image') {
            steps { sh 'docker build --target runtime -t $IMAGE .' }
        }
        stage('Deploy to Staging') {
            steps { script { deploy('shopease-staging', 8081, env.IMAGE, false) } }
        }
        stage('Smoke Test Staging') {
            steps { script { smoke('shopease-staging') } }
        }
    }
}