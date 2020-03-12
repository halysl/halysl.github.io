# ansible vault 的使用

ansible 在某些特殊的操作，例如 become 提取操作，再或者有些配置文件有机密信息，不想明文保存，那么就需要用到 vault 这个工具。它随着 ansible 发行，调用方式为 ansible-vault。

在不是非常保密严格的场合，可以只配置 2-3 个 vault 密码，去加密 ansible 用到的所有文件。

现在假设当前目录下有以下文件：

```sh
ansible.cfg
hosts
hello.yml
```

那么除了 ansible.cfg 不能被加密，其他数据都可以加密。相当于用一个密码隐藏另一堆机密数据。

## 模块说明

