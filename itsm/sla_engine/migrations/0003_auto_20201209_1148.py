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

# Generated by Django 1.11.24 on 2020-12-09 11:48
from __future__ import unicode_literals

from django.db import migrations, models


def change_fields(apps, schema_editor):
    # v2.5.8版本 sla_status 与 task_status 为 CharField类型，
    # v2.5.9 版本 为 IntegerField 类型，当数据库中有数据时，数据库中的sla_status与task_status 字符串数据会导致
    # migrate 失败，所以需要在migrate执行之前，将之前的数据进行替换。
    SlaTask = apps.get_model('sla_engine', 'SlaTask')
    
    sla_task_map = {
        "UNACTIVATED": 1,
        "RUNNING": 2,
        "PAUSED": 3,
        "STOPPED": 4
    }
    for sla_task in SlaTask.objects.all():
        # sla_status 5 表示状态正常
        sla_task.sla_status = 5
        sla_task.task_status = sla_task_map.get(sla_task.task_status, 1)
        sla_task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sla_engine', '0002_slatask_next_tick_time'),
    ]
    
    operations = [        
        migrations.RunPython(change_fields),
        
        migrations.RenameField(
            model_name='slatask',
            old_name='cost_duration',
            new_name='cost_time',
        ),
        migrations.RemoveField(
            model_name='slaactionhistory',
            name='task_id',
        ),
        migrations.RemoveField(
            model_name='slaeventlog',
            name='task_id',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='archived_duration',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='cost_percent',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='is_frozen',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='last_tick_time',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='next_tick_time',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='start_tick_time',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='stop_tick_time',
        ),
        migrations.RemoveField(
            model_name='slatask',
            name='ticket',
        ),
        migrations.AddField(
            model_name='slaactionhistory',
            name='action_id',
            field=models.IntegerField(db_index=True, default=0, verbose_name='任务ID'),
        ),
        migrations.AddField(
            model_name='slaeventlog',
            name='sla_id',
            field=models.IntegerField(db_index=True, default=0, verbose_name='SLA ID'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='begin_at',
            field=models.DateTimeField(null=True, verbose_name='任务开始计时的时间'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='end_at',
            field=models.DateTimeField(null=True, verbose_name='任务结束计时的时间'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='end_node_id',
            field=models.IntegerField(null=True, verbose_name='计时结束节点ID'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='is_replied',
            field=models.BooleanField(default=False, verbose_name='是否已响应'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='is_reply_need',
            field=models.BooleanField(default=False, verbose_name='是否需要响应'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='last_settlement_time',
            field=models.DateTimeField(null=True, verbose_name='上次结算时间'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='任务名称'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='replied_at',
            field=models.DateTimeField(null=True, verbose_name='响应时间'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='reply_cost',
            field=models.IntegerField(default=0, verbose_name='响应耗时(s)'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='reply_deadline',
            field=models.DateTimeField(null=True, verbose_name='响应截至时间'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='start_node_id',
            field=models.IntegerField(null=True, verbose_name='计时开始节点ID'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='ticket_id',
            field=models.IntegerField(null=True, verbose_name='关联的单据ID'),
        ),
        migrations.AddField(
            model_name='slatask',
            name='upgrade_at',
            field=models.DateTimeField(null=True, verbose_name='任务升级时间'),
        ),
        migrations.AlterField(
            model_name='slatask',
            name='sla_status',
            field=models.IntegerField(choices=[(1, '响应提醒'), (2, '响应超时'), (3, '处理提醒'), (4, '处理超时'), (5, '正常')], default=5, verbose_name='sla状态'),
        ),
        migrations.AlterField(
            model_name='slatask',
            name='task_status',
            field=models.IntegerField(choices=[(1, '未激活'), (2, '计时中'), (3, '暂停中'), (4, '已停止')], default=1, verbose_name='任务状态'),
        ),
    ]
