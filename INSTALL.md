# NeoShare 文件共享服务器安装部署文档

## 项目概述

NeoShare 是一个现代化的文件共享服务器，支持用户注册登录、文件上传下载、在线预览、权限管理等功能。采用 Flask 框架构建，具有响应式界面和完整的用户管理系统。

## 系统要求

- Python 3.7+
- Windows/Linux/macOS
- 至少 100MB 可用磁盘空间
- 网络连接（用于安装依赖包）

## 安装步骤

### 1. 环境准备

确保系统已安装 Python 3.7 或更高版本：

```bash
python --version
```

### 2. 克隆或下载项目

将项目文件复制到您想要安装的目录，例如 `C:\NeoShare` 或 `/opt/neoshare`

### 3. 创建虚拟环境（推荐）

在项目根目录下创建并激活虚拟环境：

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

在虚拟环境中安装项目依赖：

```bash
pip install -r requirements.txt
```

如果遇到依赖安装问题，可以尝试升级 pip：

```bash
python -m pip install --upgrade pip
```

### 5. 配置数据库

首次运行时，系统会自动创建 SQLite 数据库文件。确保 `instance` 目录存在：

```bash
mkdir instance
```

### 6. 运行服务器

执行以下命令启动服务器：

```bash
python run.py
```

服务器将在 `http://127.0.0.1:5000` 启动，默认使用 5000 端口。

## 配置说明

### 环境变量

项目支持以下环境变量配置：

- `SECRET_KEY`: 应用程序密钥（默认为随机生成）
- `DATABASE_URL`: 数据库连接字符串（默认使用 SQLite）
- `UPLOAD_FOLDER`: 文件上传目录（默认为 `uploads`）
- `MAX_CONTENT_LENGTH`: 最大上传文件大小（默认为 100MB）

### 默认管理员账户

首次启动后，系统会自动创建默认管理员账户：
- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@neoshare.com`

**安全提醒：** 首次登录后请立即修改默认管理员密码。

## 使用说明

### 用户功能
1. **注册/登录**: 新用户可注册账户，已注册用户可登录
2. **文件上传**: 登录用户可上传文件到个人空间或公共空间
3. **文件管理**: 查看、下载、删除自己上传的文件
4. **个人资料**: 修改个人信息和头像

### 管理员功能
1. **用户管理**: 查看、编辑、删除用户账户
2. **文件管理**: 管理所有用户上传的文件
3. **系统监控**: 查看系统状态和统计数据

### 访问控制
- 公共文件: 所有用户可查看和下载
- 私有文件: 仅文件所有者可访问
- 管理员: 可访问所有文件和用户数据

## 部署到生产环境

### 使用 Gunicorn (Linux/macOS)

1. 安装 Gunicorn:
```bash
pip install gunicorn
```

2. 启动服务:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 使用 Windows 服务

1. 安装 `pywin32`:
```bash
pip install pywin32
```

2. 创建服务脚本并注册为 Windows 服务

### 反向代理配置

推荐使用 Nginx 作为反向代理:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排除

### 常见问题

1. **端口被占用**
   - 检查是否有其他服务占用 5000 端口
   - 修改 `run.py` 中的端口号

2. **权限问题**
   - 确保对 `uploads` 和 `instance` 目录有读写权限
   - 在 Linux 系统上可能需要调整目录权限

3. **数据库连接错误**
   - 检查 `instance` 目录是否存在
   - 确认数据库文件路径正确

4. **CDN 资源加载失败**
   - 检查网络连接
   - 确认 `app/templates/base.html` 中的 CDN 链接

### 日志查看

应用日志会输出到控制台，如需记录到文件，可重定向输出：

```bash
python run.py > app.log 2>&1
```

## 备份与迁移

### 数据备份

1. **数据库备份**: 复制 `instance/neoshare.db` 文件
2. **文件备份**: 复制整个 `uploads` 目录
3. **配置备份**: 备份环境变量配置

### 迁移步骤

1. 将项目文件复制到新服务器
2. 安装 Python 依赖
3. 复制数据库文件到 `instance` 目录
4. 复制上传的文件到 `uploads` 目录
5. 根据新环境调整配置
6. 启动服务

## 安全建议

1. **修改默认管理员密码**
2. **使用 HTTPS** (生产环境)
3. **限制文件上传类型**
4. **定期备份数据**
5. **更新依赖包** (定期运行 `pip list --outdated`)

## 更新版本

1. 备份数据库和上传文件
2. 下载新版本代码
3. 安装新的依赖包
4. 运行数据库迁移（如有）
5. 重启服务

## 技术支持

如遇到问题，请检查：
- Python 版本兼容性
- 依赖包版本
- 系统权限设置
- 网络连接状态

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。

---

**注意**: 这是一个开发版本，生产部署前请确保已完成安全配置。