# yarn 安装和使用

## 安装

```sh
# macOS 安装
# 方法1
brew install yarn
# 方法2
curl -o- -L https://yarnpkg.com/install.sh | bash

# Ubuntu/Debian
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt update && sudo apt install yarn

# CentOS / Fedora / RHEL
curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
sudo yum install yarn
```
