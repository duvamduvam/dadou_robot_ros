pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    DOCKER_IMAGE = env.DOCKER_IMAGE ?: "dadou_robot"
    DOCKER_TAG = env.DOCKER_TAG ?: "${env.BRANCH_NAME ?: 'main'}-${env.BUILD_NUMBER}"
    DOCKER_CONTEXT = env.DOCKER_CONTEXT ?: "."
    DOCKERFILE = env.DOCKERFILE ?: "conf/docker/jenkins/Dockerfile-jenkins"
  }

  stages {
    stage('Run CI script on builder host') {
      steps {
        sh """
          ssh -o StrictHostKeyChecking=no ${env.JENKINS_REMOTE_USER ?: 'pi'}@${env.JENKINS_REMOTE_HOST ?: '172.17.0.1'} \\
            "REPO_URL='${env.REPO_URL ?: 'git@github.com:duvamduvam/dadou_robot_ros.git'}' \\
            REPO_BRANCH='${env.REPO_BRANCH ?: 'main'}' \\
            PYTHON_REQUIREMENTS='${env.PYTHON_REQUIREMENTS ?: 'requirements.txt'}' \\
            TEST_COMMAND='${env.TEST_COMMAND ?: 'pytest -q'}' \\
            DOCKER_IMAGE='$DOCKER_IMAGE' \\
            DOCKER_TAG='$DOCKER_TAG' \\
            DOCKER_CONTEXT='$DOCKER_CONTEXT' \\
            DOCKERFILE='$DOCKERFILE' \\
            WORKSPACE_ROOT='${env.WORKSPACE_ROOT ?: '/home/pi/jenkins-workspace'}' \\
            KEEP_WORKDIR='${env.KEEP_WORKDIR ?: '1'}' \\
            ${env.CI_SCRIPT_PATH ?: '/var/jenkins_home/scripts/run_ci_pipeline.sh'}"
        """
      }
    }

    if (env.DOCKER_PUSH_ENABLED?.toBoolean()) {
      stage('Docker Push') {
        steps {
          sh '''
            docker push "${DOCKER_IMAGE}:${DOCKER_TAG}"
          '''
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
