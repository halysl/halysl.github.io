使用 python3，即 `-e ansible_python_interpreter=/usr/bin/python3`

setup 获得 facts，根据特性作为 when 判断条件执行 task

通过 template 方式获得 `可渲染的配置文件` 以及 `有参数的 shell脚本`

通过 vars_files 这个 key 指定需要加载的 var 文件，其 value 为一个 list

通过 handler 方式触发服务启动

通过 become 设置为 yes 触发提权操作，在 hosts 里指定密码，并用 vault 模块加密
