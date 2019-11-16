---
layout: post
title: Go 的第一个爬虫
categories: [Go, 爬虫]
description: Go 的第一个爬虫
keywords: 
---

# Go 的第一个爬虫

使用 Go 实现了第一个爬虫，只使用了标准模块，无第三方模块。整体难度较低，获取 `http.cat` 里所有猫的照片，先从入口进入，正则匹配相关图片的 url，然后通过 file.Write 实现内容的下载，在整个过程中，使用了 http、bytes、ioutil、os、regexp 等模块，对 Go 的文件模块、路径模块和正则模块有了简单的了解。

## 定义结构体，保存数据

```Go
var base_url = "https://http.cat"

type cat struct {
	// 一个结构体代表一个爬取项目
	name, url string
}
```

## 爬取页面代码

```Go
func httpGet(url string) (data []byte, statusCode int) {
	// get 请求从 url 拿数据，返回 []byte, status code
	fmt.Printf("date:%s\turl:%s\n", time.Now(), url)
	resp, err := http.Get(url)
	if err != nil {
		statusCode = -100
		return data, statusCode
	}
	defer resp.Body.Close()
	data, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		statusCode = -200
		return data, statusCode
	}
	statusCode = resp.StatusCode
	return data, statusCode
}
```

直接返回 []byte 是方便外部处理更方便。可以直接写入，或者 string([]byte) 转换为字符串。

## 正则拿到 url

```Go
func regexParse(data string) []cat {
	// 从爬虫结果中通过正则提取所有目标数据的 name 和 url
	imageExp := regexp.MustCompile(`\((/images/\d{3}.jpg)\)"></div><div class="Thumbnail_content__2eR9q"><div class="Thumbnail_title__2iqYK">(\d{3})</div><p>([\w-´ ]*)`)
	res := make([]cat, 0)
	tds := imageExp.FindAllStringSubmatch(data, 100)
	for _, value := range tds {
		var buffer1 bytes.Buffer
		var buffer2 bytes.Buffer
		buffer1.WriteString(value[2])
		buffer1.WriteString("_")
		buffer1.WriteString(value[3])
		name := buffer1.String()
		buffer2.WriteString(base_url)
		buffer2.WriteString(value[1])
		url := buffer2.String()
		res = append(res, cat{name, url})
	}
	return res
}
```

通过 bytes.Buffer 实现字符串的拼接，还有其他几种拼接方案。正则通过 [regular expressions 101](https://regex101.com) 测试。

## 获得图片保存路径

```Go
func getPicPath() string {
	// 获得图片保存目录
	pwd,  _ := os.Getwd()
	pic_dir := path.Join(pwd, "catchcats", "pic")
	return pic_dir
}
```

## 保存图片

```Go
func write_pic(base_path, name string, data []byte) {
	// 写入文件，形成图片
	file, err := os.Create(base_path + "/" + name + ".jpg")
	if err != nil{
		log.Fatalln(err)
	}
	defer file.Close()
	_, err = file.Write(data)
	if err != nil {
		log.Fatalln(err)
	}
}
```

## 整合起来

```Go
func Run() {
	data, statusCode := httpGet(base_url)
	if statusCode == 200 {
		res := regexParse(string(data))
		pic_path := getPicPath()
		for _, c := range res {
			data, statusCode = httpGet(c.url)
			if statusCode == 200 {
				write_pic(pic_path, c.name, data)
			} else {
				fmt.Printf("url: %s\tstatus code: %d\n", c.url, statusCode)
			}
		}
	} else {
		fmt.Printf("url: %s\tstatus code: %d\n", base_url, statusCode)
	}
}
```

## 总结

整体难度不大，花了大概三小时实现，主要是各种模块的资料查找，下面是参考资料：

- [Go 获取当前目录路径](https://juejin.im/post/5cd983e16fb9a031f61d973b)
- [path/filepath — 兼容操作系统的文件路径操作](https://books.studygolang.com/The-Golang-Standard-Library-by-Example/chapter06/06.2.html)
- [golang 几种字符串的拼接方式](https://blog.csdn.net/iamlihongwei/article/details/79551259)
- [Go实战--golang中读写文件的几种方式](https://blog.csdn.net/wangshubo1989/article/details/74777112)
- [Golang 中对文件 file 操作方法总结](https://blog.csdn.net/netdxy/article/details/71335094)
- [Go-下载网上图片](https://studygolang.com/articles/5478)
- [Go-入门指南 4.8 时间和日期](https://www.kancloud.cn/kancloud/the-way-to-go/72463)

Go 挺有意思的，希望能坚持下去。
