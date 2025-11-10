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
          env.GITHUB_NOTIFY_ENABLED = env.GITHUB_NOTIFY_ENABLED?.trim() ?: 'true'
          env.GITHUB_NOTIFY_ACCOUNT = env.GITHUB_NOTIFY_ACCOUNT?.trim() ?: 'duvamduvam'
          env.GITHUB_NOTIFY_REPO = env.GITHUB_NOTIFY_REPO?.trim() ?: 'dadou_robot_ros'
          env.GITHUB_NOTIFY_CREDENTIALS_ID = env.GITHUB_NOTIFY_CREDENTIALS_ID?.trim() ?: 'github-token4'
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
          'SUCCESS': 'success',
          'FAILURE': 'failure',
          'UNSTABLE': 'failure',
          'ABORTED': 'error',
          'NOT_BUILT': 'pending'
        ]
        def githubStatus = statusMap.get(rawStatus, 'error')

        def extractRepoSlug = { rawUrl ->
          if (!rawUrl) {
            return ''
          }
          return rawUrl
            .replaceFirst('^.+github.com[:/]', '')
            .replaceFirst(/\.git$/, '')
        }

        def repoSlug = extractRepoSlug(env.GIT_URL)
        if (!repoSlug) {
          repoSlug = extractRepoSlug(env.REPO_URL)
        }
        def slugParts = repoSlug ? repoSlug.tokenize('/') : []
        def derivedOwner = slugParts.size() >= 1 ? slugParts[0] : ''
        def derivedRepo = slugParts.size() >= 2 ? slugParts[1] : (slugParts ? slugParts[0] : '')

        def githubOwner = env.GITHUB_NOTIFY_ACCOUNT?.trim()
        if (!githubOwner) {
          githubOwner = derivedOwner
        }
        def githubRepo = env.GITHUB_NOTIFY_REPO?.trim()
        if (!githubRepo) {
          githubRepo = derivedRepo
        }
        def commitSha = env.GIT_COMMIT?.trim()
        if (!commitSha) {
          try {
            commitSha = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
          } catch (Exception ignored) {
            commitSha = ''
          }
        }
        def githubCreds = env.GITHUB_NOTIFY_CREDENTIALS_ID?.trim()
        def notifyEnabled = env.GITHUB_NOTIFY_ENABLED?.toBoolean()

        if (notifyEnabled && githubOwner && githubRepo && commitSha && githubCreds) {
          echo "GitHub notify metadata -> owner: ${githubOwner}, repo: ${githubRepo}, sha: ${commitSha}"
          withCredentials([string(credentialsId: githubCreds, variable: 'GITHUB_TOKEN')]) {
            sh label: 'GitHub status update', script: """#!/usr/bin/env bash
set -euo pipefail
curl -sSf -X POST https://api.github.com/repos/${githubOwner}/${githubRepo}/statuses/${commitSha} \\
  -H 'Authorization: Bearer '"\${GITHUB_TOKEN}" \\
  -H 'Accept: application/vnd.github+json' \\
  -d '{
    "state": "${githubStatus}",
    "target_url": "${env.BUILD_URL}",
    "description": "Build ${githubStatus}",
    "context": "Jenkins CI"
  }'
"""
          }
        } else {
          echo 'Skipping GitHub status update (disabled or missing metadata/credentials).'
        }
      }
      cleanWs()
    }
  }
}
