# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")
path = ""
ASSET_PATH = "apps//"

if "github_user_tildagon_miner" in apps:
    ASSET_PATH = "/apps/github_user_tildagon_miner/"

if "miner" in apps:
    ASSET_PATH = "apps/miner/"
