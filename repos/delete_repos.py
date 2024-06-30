import requests
import json

# Load the GitHub token from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)


GITHUB_USERNAME = config['GITHUB_USERNAME']
GITHUB_TOKEN = config['GITHUB_TOKEN']


def get_orgs():
    url = 'https://api.github.com/user/orgs'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to retrieve organizations')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return []


def get_org_repos(org_name):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve repositories for organization: {org_name}')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return []


def delete_repo(org_name, repo_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f'Successfully deleted repository: {repo_name}')
    elif response.status_code == 403:
        print(f'Failed to delete repository: {repo_name}')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        print('This is likely due to insufficient permissions or token scope.')
    else:
        print(f'Failed to delete repository: {repo_name}')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')


def main():
    orgs = get_orgs()
    for org in orgs:
        org_name = org['login']
        print(f'Processing organization: {org_name}')
        repos = get_org_repos(org_name)
        for repo in repos:
            repo_name = repo['name']
            print(f'Deleting repository {repo_name} in organization {org_name}')
            delete_repo(org_name, repo_name)


if __name__ == '__main__':
    main()
