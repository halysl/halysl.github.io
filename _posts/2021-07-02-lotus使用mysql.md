# Lotus 使用 MySQL 替代本地扫描

## 创建 mysql 服务

```
docker run --name lotus-mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -d mysql
```

## 创建数据库

```
# 需要等待一会，等待mysql服务启动
sleep 30
docker exec -it lotus-mysql bash

mysql -u root -p

CREATE DATABASE IF NOT EXISTS SL DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

## 获取数据，生成dump.sql

```sh
#! /bin/bash
storage_path_array=(""
    "/minio/"
    "/nfs/store03/t07637_32G_newtest")

# create file
file_name=/tmp/dump.sql
touch ${file_name}

# create table
cat>"${file_name}"<<EOF
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_storage_path
-- ----------------------------
DROP TABLE IF EXISTS \`t_storage_path\`;
CREATE TABLE \`SL\`.\`t_storage_path\`  (
  \`id\` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  \`storage_path\` varchar(255) NOT NULL DEFAULT '' COMMENT '存储路径',
  \`create_time\` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  \`update_time\` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (\`id\`)
 ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='存储路径表';


-- ----------------------------
-- Table structure for t_sector_storage
-- ----------------------------
DROP TABLE IF EXISTS \`t_sector_storage\`;
CREATE TABLE \`SL\`.\`t_sector_storage\`  (
    \`id\` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
    \`sector_id\` varchar(255) NOT NULL DEFAULT '' COMMENT '扇区id',
    \`storage_path_id\` int(11) unsigned NOT NULL DEFAULT 1 COMMENT '存储路径id',
    \`state\` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1:正常  0:已删除',
    \`worker_name\` varchar(255) NOT NULL DEFAULT '' COMMENT 'worker名称',
    \`create_time\` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    \`update_time\` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (\`id\`),
    INDEX \`index_sector_id\`(\`sector_id\`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='扇区与存储路径关系表';

EOF

# insert storage path
cat>>"${file_name}"<<EOF
-- ----------------------------
-- Records of t_storage_path
-- ----------------------------
EOF

echo "BEGIN;" >> "${file_name}"

for element in ${storage_path_array[*]}
do
  if [ -z $element ];
  then
    continue
  fi
  printf "INSERT INTO t_storage_path(storage_path) VALUES(\"%s\");\n" ${element} >> "${file_name}"
done

echo "COMMIT;" >> "${file_name}"
echo "SET FOREIGN_KEY_CHECKS = 1;" >> "${file_name}"
echo ""  >> "${file_name}"

# insert sector path
cat>>"${file_name}"<<EOF
-- ----------------------------
-- Records of t_sector_storage
-- ----------------------------
EOF

echo "BEGIN;" >> "${file_name}"

for i in "${!storage_path_array[@]}";
do
  if [ $i -eq 0 ];
  then
    continue
  fi
  sector_arr=`ls -F ${storage_path_array[$i]}/sealed`
  for sector in ${sector_arr[*]}
  do
    sector_id=`echo $sector | sed "s/*//"`
    if [[ ${sector_id} == "fetching/" ]]
    then
      continue
    fi
    if [[ ${sector_id} =~ "st-base" ]]
    then
      continue
    fi
    printf "INSERT INTO t_sector_storage(sector_id, storage_path_id, state, worker_name) VALUES(\"%s\",%d, 1,\"null\");\n" ${sector_id} ${i} >> "${file_name}"
  done
done

echo "COMMIT;" >> "${file_name}"
echo "SET FOREIGN_KEY_CHECKS = 1;" >> "${file_name}"

```

## mysql source

```
docker cp /tmp/dump.sql lotus-mysql:/tmp/
docker exec -it lotus-mysql bash

mysql -u root -p SL < /tmp/dump.sql
```
