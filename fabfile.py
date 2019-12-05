from fabric import task

PROJECT_DIR = '/home/projects/django_instagram'
VIRTUALENV_ACTIVATE_CMD = 'source /home/projects/django_instagram/venv/bin/activate'
USERNAME = 'root'
HOSTNAME = '157.230.99.70'
hosts = [f'{USERNAME}@{HOSTNAME}']


@task(hosts=hosts)
def deploy(connection):
    connection.run(f'cd {PROJECT_DIR}; git pull')
    connection.run(f'{VIRTUALENV_ACTIVATE_CMD}; cd {PROJECT_DIR}; pip3 install -r requirements.txt')
    connection.run(f'{VIRTUALENV_ACTIVATE_CMD}; cd {PROJECT_DIR}/instagram; python3 manage.py collectstatic --noinput')
    connection.run('supervisorctl restart all')
