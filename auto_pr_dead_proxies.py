# auto_pr_dead_proxies.py
import yaml
import os
import subprocess

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(data, path):
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def remove_dead_proxies():
    if not os.path.exists("alive_proxies.yaml") or not os.path.exists("proxies.yaml"):
        print("Missing required YAML files.")
        return False

    all_proxies = load_yaml("proxies.yaml").get("proxies", [])
    alive_proxies = load_yaml("alive_proxies.yaml").get("proxies", [])

    alive_set = {(p['server'], p['port']) for p in alive_proxies}

    cleaned = [p for p in all_proxies if (p['server'], p['port']) in alive_set]

    save_yaml({"proxies": cleaned}, "proxies.yaml")
    return True

def create_branch_commit_push():
    subprocess.run(["git", "checkout", "-b", "remove-dead-proxies"])
    subprocess.run(["git", "add", "proxies.yaml"])
    subprocess.run(["git", "commit", "-m", "🔥 Remove dead proxies"])
    subprocess.run(["git", "push", "--set-upstream", "origin", "remove-dead-proxies"])

def create_pull_request():
    subprocess.run([
        "gh", "pr", "create",
        "--title", "🔥 Remove dead proxies",
        "--body", "This PR automatically removes all dead proxies from proxies.yaml.",
        "--base", "main",
        "--head", "remove-dead-proxies"
    ])

def main():
    if remove_dead_proxies():
        create_branch_commit_push()
        create_pull_request()
    else:
        print("❌ Failed to update proxies.yaml")

if __name__ == '__main__':
    main()
