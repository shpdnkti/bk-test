# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BK-ITSM 蓝鲸流程服务 available.

Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.

BK-ITSM 蓝鲸流程服务 is licensed under the MIT License.

License for BK-ITSM 蓝鲸流程服务:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Generated by Django 1.11.24 on 2019-11-20 19:09
from __future__ import unicode_literals

from django.db import migrations, models

from itsm.component import fields


class Migration(migrations.Migration):

    dependencies = [
        ('iadmin', '0006_auto_20190919_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=128, verbose_name='关键字')),
                ('value', fields.IOField(verbose_name='值')),
                (
                    'type',
                    models.CharField(
                        choices=[('string', '字符串'), ('hash', '哈希值'), ('list', '列表'), ('set', '集合'), ('zset', '有序集合')],
                        default='string',
                        max_length=32,
                        verbose_name='类型',
                    ),
                ),
                ('expire_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='过期时间')),
            ],
            options={'verbose_name': '数据存储', 'verbose_name_plural': '数据存储',},
        ),
    ]
