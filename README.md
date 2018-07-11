## 运行开发环境
- 创建数据库并修改settings.py中相应配置(数据库配置)
- 创建python虚拟环境: python2.7
- 安装依赖包: pip install -r requirements.txt
- 初始化数据库: 
```
python manage.py makemigrations
python manage.py migrate
```
- 创建初始账户: python manage.py createsuperuser
- 运行项目： python manage.py runserver