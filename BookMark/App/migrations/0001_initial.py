# Generated by Django 3.2 on 2021-04-29 08:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=1200, primary_key=True, serialize=False, verbose_name='ISBN')),
                ('publisher', models.CharField(max_length=128, null=True, verbose_name='出版商')),
                ('pubdate', models.DateField(null=True, verbose_name='出版日期')),
                ('image_medium', models.CharField(max_length=1200, null=True, verbose_name='书的图像(中)')),
                ('image_large', models.CharField(max_length=1000, null=True, verbose_name='书的图像(大)')),
                ('author', models.CharField(max_length=200, null=True, verbose_name='作者')),
                ('subTitle', models.CharField(max_length=1000, null=True, verbose_name='副标题')),
                ('mainTitle', models.CharField(max_length=1000, null=True, verbose_name='主标题')),
                ('summary', models.CharField(max_length=2000, null=True, verbose_name='总结')),
                ('pages', models.IntegerField(null=True, verbose_name='页数')),
            ],
            options={
                'verbose_name': '书籍',
                'verbose_name_plural': '书籍',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conception', models.CharField(max_length=200, null=True, verbose_name='概念')),
                ('explanation', models.CharField(max_length=2000, null=True, verbose_name='解释')),
                ('example', models.CharField(max_length=2000, null=True, verbose_name='举例')),
                ('resemblence', models.CharField(max_length=2000, null=True, verbose_name='类似的概念')),
                ('QA', models.CharField(max_length=2000, null=True, verbose_name='自问自答')),
                ('page', models.IntegerField(null=True, verbose_name='所在页面')),
                ('time', models.DateField(auto_now_add=True, null=True)),
                ('like_num', models.IntegerField(default=0, null=True, verbose_name='点赞数')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='所含词条', to='App.book', verbose_name='所在书名')),
            ],
            options={
                'verbose_name': '词条',
                'verbose_name_plural': '词条',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick_name', models.CharField(max_length=128, null=True, verbose_name='昵称')),
                ('profile_img', models.CharField(max_length=128, null=True, verbose_name='头像')),
                ('email', models.EmailField(max_length=128, null=True, verbose_name='邮件')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='likeInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True, null=True)),
                ('entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='App.entry', verbose_name='点赞的词条')),
                ('user_like', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userlike', to=settings.AUTH_USER_MODEL, verbose_name='点赞者')),
                ('user_liked', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userliked', to=settings.AUTH_USER_MODEL, verbose_name='被点赞者')),
            ],
            options={
                'verbose_name': '点赞信息',
                'verbose_name_plural': '点赞信息',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='users_write',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_write', to=settings.AUTH_USER_MODEL, verbose_name='词条作者'),
        ),
    ]