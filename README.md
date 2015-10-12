### 演示: [xianzhi.ifujun.com](#)

这是我初学Django时写的一个demo,取个名字，叫“闲置”，此为练手之作，只能供新手学习，不能用于生产环境。

**Require: **
**Django \>=1.8.0**
**Mysql**


数据库配置修改位置：
**Xianzhi/Xianzhi/settings.py**
修改下方的数据库名称、用户名、密码、Host和端口号

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'xianzhi',
	        'USER': 'root',
	        'PASSWORD': 'fujun',
	        'HOST':'localhost',
	        'PORT': '3306',
	    }
	}

