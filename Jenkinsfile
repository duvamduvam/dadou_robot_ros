pipeline {
  agent any

  options {
    timestamps()
  }

  stages {
    stage('Prepare defaults') {
      steps {
        script {
          env.DOCKER_IMAGE = env.DOCKER_IMAGE?.trim() ?: 'dadou_robot'
          env.DOCKER_TAG = env.DOCKER_TAG?.trim() ?: "${env.BRANCH_NAME ?: 'main'}-${env.BUILD_NUMBER}"
          env.DOCKER_CONTEXT = env.DOCKER_CONTEXT?.trim() ?: '.'
          env.DOCKERFILE = env.DOCKERFILE?.trim() ?: 'conf/docker/jenkins/Dockerfile-jenkins'
          env.JENKINS_REMOTE_USER = env.JENKINS_REMOTE_USER?.trim() ?: 'pi'
          env.JENKINS_REMOTE_HOST = env.JENKINS_REMOTE_HOST?.trim() ?: '172.17.0.1'
          env.REPO_URL = env.REPO_URL?.trim() ?: 'git@github.com:duvamduvam/dadou_robot_ros.git'
          env.REPO_BRANCH = env.REPO_BRANCH?.trim() ?: 'main'
          env.PYTHON_REQUIREMENTS = env.PYTHON_REQUIREMENTS?.trim() ?: 'requirements.txt'
          env.TEST_COMMAND = env.TEST_COMMAND?.trim() ?: 'pytest -q /home/ros2_ws/src/robot/robot/tests --ignore=/home/ros2_ws/src/robot/robot/tests/sandbox'
          env.WORKSPACE_ROOT = env.WORKSPACE_ROOT?.trim() ?: '/home/pi/jenkins-workspace'
          env.KEEP_WORKDIR = env.KEEP_WORKDIR?.trim() ?: '1'
          def rawScriptPath = env.CI_SCRIPT_PATH?.trim()
          if (!rawScriptPath || rawScriptPath.isEmpty()) {
            env.CI_SCRIPT_PATH = '/home/pi/jenkins/scripts/run_ci_pipeline.sh'
          } else if (rawScriptPath == '/var/jenkins_home/scripts/run_ci_pipeline.sh') {
            env.CI_SCRIPT_PATH = '/home/pi/jenkins/scripts/run_ci_pipeline.sh'
          } else {
            env.CI_SCRIPT_PATH = rawScriptPath
          }
          env.DOCKER_PUSH_ENABLED = env.DOCKER_PUSH_ENABLED?.trim() ?: 'false'
        }
      }
    }

    stage('Run CI script on builder host') {
      steps {
        sh """#!/usr/bin/env bash
          ssh -o StrictHostKeyChecking=no ${env.JENKINS_REMOTE_USER}@${env.JENKINS_REMOTE_HOST} \\
            "REPO_URL='${env.REPO_URL}' \\
            REPO_BRANCH='${env.REPO_BRANCH}' \\
            PYTHON_REQUIREMENTS='${env.PYTHON_REQUIREMENTS}' \\
            TEST_COMMAND='${env.TEST_COMMAND}' \\
            DOCKER_IMAGE='${env.DOCKER_IMAGE}' \\
            DOCKER_TAG='${env.DOCKER_TAG}' \\
            DOCKER_CONTEXT='${env.DOCKER_CONTEXT}' \\
            DOCKERFILE='${env.DOCKERFILE}' \\
            WORKSPACE_ROOT='${env.WORKSPACE_ROOT}' \\
            KEEP_WORKDIR='${env.KEEP_WORKDIR}' \\
            ${env.CI_SCRIPT_PATH}"
        """
      }
    }

    stage('Docker Push') {
      when {
        expression { env.DOCKER_PUSH_ENABLED?.toBoolean() }
      }
      steps {
        sh """#!/usr/bin/env bash
          docker push "${env.DOCKER_IMAGE}:${env.DOCKER_TAG}"
        """
      }
    }
  }

  post {
    always {
      script {
        def rawStatus = (currentBuild.currentResult ?: 'SUCCESS').toString()
        def statusMap = [
          'SUCCESS': 'SUCCESS',
          'FAILURE': 'FAILURE',
          'UNSTABLE': 'FAILURE',
          'ABORTED': 'ERROR',
          'NOT_BUILT': 'PENDING'
        ]
        def githubStatus = statusMap.get(rawStatus, 'ERROR')
        def repoSlug = ''
        if (env.GIT_URL) {
          repoSlug = env.GIT_URL
            .replaceFirst('^.+github.com[:/]', '')
            .replaceFirst(/\.git$/, '')
        }
        def slugParts = repoSlug ? repoSlug.tokenize('/') : []
        def githubOwner = (slugParts.size() >= 2) ? slugParts[-2] : ''
        def githubRepo = (slugParts.size() >= 1) ? slugParts[-1] : ''
        def commitSha = env.GIT_COMMIT?.trim()
        if (!commitSha) {
          try {
            commitSha = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
          } catch (Exception ignored) {
            commitSha = ''
          }
        }
        try {
          if (githubOwner && githubRepo && commitSha) {
            githubNotify(
              context: 'Jenkins CI',
              status: githubStatus,
              description: "Build ${githubStatus.toLowerCase()}",
              targetUrl: env.BUILD_URL,
              account: githubOwner,
              repo: githubRepo,
              sha: commitSha
            )
          } else {
            echo 'Missing git metadata (owner/repo/sha); skipping GitHub commit status update.'
          }
        } catch (hudson.AbortException e) {
          echo "githubNotify failed: ${e.message}"
        } catch (Exception e) {
          def reason = e.toString()
          if (reason.contains('MissingStepException') || reason.contains('MissingMethodException')) {
            echo 'githubNotify step unavailable; skipping GitHub commit status update.'
          } else {
            echo "githubNotify failed: ${e.message}"
          }
        }
      }
      cleanWs()
    }
  }
}
