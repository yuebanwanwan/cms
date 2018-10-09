from django import forms

class LoginForm(forms.Form):
	
	uid = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control' ,'id':'uid', 'placeholder': 'Username'}))
	pwd = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'pwd', 'placeholder': 'Password'}))

class RegisterForm(forms.Form):
	username = forms.CharField(label='username', max_length=100,
		widget=forms.TextInput(attrs={'id':'username', 'onblur': 'authentication()'}))
	email = forms.EmailField()
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

class SetInfoForm(forms.Form):
	username = forms.CharField()

class CommmentForm(forms.Form):
	comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '77', 'rows': '8'}))

class SearchForm(forms.Form):
	keyword = forms.CharField(widget=forms.TextInput)

# form.Form与HTML元素对应关系
# 1 首先全部都是input元素
# 2 字段名字就是对应input元素的name属性的值
# 3 forms.PasswordInput()与forms.EmailField()区别在于对应的input元素的type属性的值有所不同，比如forms.CharField()----type="password" /....="text"
#   forms.CharFiled()则是默认的,是一个可扩展的类型
# 4 label='username'会自动在input元素前自动添加该文本
# 5 widget用来设置input元素的type属性的值以及添加其他属性以及该添加属性的值