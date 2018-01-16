# Configuration file for Jupyter Hub
# Need to test DockerHub push

c = get_config()

c.JupyterHub.log_level = 10

from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator

c.Authenticator.whitelist = whitelist = set()
c.JupyterHub.admin_users = admin = set()

import os
import sys

join = os.path.join

here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
sys.path.insert(0, root)

with open(join(root, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# ssl config
ssl = join(root, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
# Set up spawner
c.JupyterHub.spawner_class = 'ecsspawner.ECSSpawner'

# options
c.ECSSpawner.cluster_name = 'jupyter-cluster'
c.ECSSpawner.task_definition = 'jupyter-notebook:1'