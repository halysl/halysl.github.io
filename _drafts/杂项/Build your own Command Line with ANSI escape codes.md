http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#ascii-progress-bar

# 通过 ANSI 转义序列构建你个人的命令行

每个人都习惯于在终端上打印输出，程序会随着新文本的出现而滚动，但这并不是您所能做的：您的程序可以为文本着色，上下左右移动光标或清除屏幕的一部分如果您以后要重新打印它们。这就是让Git之类的程序实现其动态进度指示器，让Vim或Bash实现其编辑器的功能，这些编辑器使您无需滚动终端即可修改已显示的文本。
