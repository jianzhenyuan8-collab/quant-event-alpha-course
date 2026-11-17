# 发布到自己的 GitHub 仓库

> 当前 GitHub 连接显示账号 `jianzhenyuan8-collab`，但对话连接未开放**创建仓库**接口；先由仓库所有者在 GitHub 网站创建一个空的私有仓库，然后可将本项目推送进去。

## 在 GitHub 创建仓库

打开 https://github.com/new ，确认网页右上角当前账号就是你想使用的账号。仓库建议名 `quant-event-alpha-course`，可先设为 **Private**。创建时**不要勾选初始化 README、.gitignore、License**，因为这里已包含这些文件（尚未添加License）。

## 本地推送（安装 Git 后）

先把下载的ZIP解压并进入项目根目录：

```bash
git init
git checkout -b main
git add .
git commit -m "Add 60-chapter quantitative research course and practice labs"
git remote add origin https://github.com/<你的GitHub用户名>/quant-event-alpha-course.git
git push -u origin main
```

将URL中的 `<你的GitHub用户名>` 替换为你实际使用的用户名。若网页上创建了不同仓库名，按实际名称修改URL。GitHub不支持直接使用账户密码认证Git命令，请使用Git Credential Manager、SSH或有正确权限的凭证。

## 验收

打开新仓库，检查 `SYLLABUS.md` 有60章链接，`chapters/`下有60个编号文档，`labs/`下有16个实验程序；打开 `Actions` 查看测试。

默认实验不连接实盘，不包含私钥、API密钥或账户凭证。
