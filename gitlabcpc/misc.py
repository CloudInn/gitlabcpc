from cement.utils import shell

def populate_gitlab_config():

    config = {}
    config['secret'] = shell.Prompt("Enter your Gitlab secret key:").input
    config['url'] = shell.Prompt("Enter the gitlab instance URL:").input
    config['name'] = shell.Prompt("Enter this gitlab instance's unique name:", default="default").input

    return config
