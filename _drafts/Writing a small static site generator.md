https://blog.thea.codes/a-small-static-site-generator/

# 编写一个小型静态网站生成器

大概有一百多种用Python编写的静态站点生成器（甚至还有其他语言编写的静态站点生成器）。

所以我决定写我自己的。为什么？好吧，我只是想。我希望将自己的博客从Ghost移开，并且希望保持真正的简约性。我决定使用GitHub Pages托管输出，因为他们最近宣布支持自定义域的SSL。

## 渲染内容
每个静态网站生成器都需要采用某种源格式（例如Markdown或ReStructuredText）并将其转换为HTML。自从我离开Ghost以来，我决定坚持Markdown。

自从我最近将Github风格的Markdown渲染集成到Warehouse中以来，我决定使用为该cmarkgfm创建的基础库。使用以下方式将Markdown渲染为HTML cmarkgfm：

```python
import cmarkgfm


def render_markdown(content: str) -> str:
    content = cmarkgfm.markdown_to_html_with_extensions(
        content,
        extensions=['table', 'autolink', 'strikethrough'])
    return content
```
