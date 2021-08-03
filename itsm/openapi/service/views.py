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

from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response

from blueapps.account.decorators import login_exempt
from itsm.component.utils.basic import dotted_name
from itsm.component.drf import viewsets as component_viewsets
from itsm.component.drf.mixins import ApiGatewayMixin
from itsm.component.exceptions import ServicePartialError
from itsm.component.exceptions import ObjectNotExist
from itsm.openapi.service.serializers import ServiceRetrieveSerializer, ServiceSerializer
from itsm.service.models import CatalogService, Service, ServiceCatalog
from itsm.workflow.models import Workflow
from itsm.component.constants import role
from itsm.role.models import UserRole


@method_decorator(login_exempt, name='dispatch')
class ServiceViewSet(ApiGatewayMixin, component_viewsets.AuthModelViewSet):
    """
    服务项视图集合
    """

    queryset = Service.objects.filter(is_valid=True)
    serializer_class = ServiceSerializer
    permission_free_actions = ("get_services", "get_service_detail", "get_service_catalogs")

    @action(detail=False, methods=['get'], serializer_class=ServiceSerializer)
    def get_services(self, request):
        """
        服务项列表
        """

        queryset = self.queryset.all()

        catalog_id = request.query_params.get('catalog_id')
        if catalog_id:
            queryset = queryset.filter(
                id__in=CatalogService.objects.filter(catalog_id=catalog_id).values_list('service', flat=True)
            )

        service_type = request.query_params.get('service_type')
        if service_type:
            queryset = queryset.filter(key=service_type)

        display_type = request.query_params.get('display_type')
        if display_type:
            queryset = queryset.filter(display_type=display_type)

        display_role = request.query_params.get('display_role')
        if display_role:
            queryset = queryset.filter(display_role__contains=dotted_name(display_role))

        return Response(self.serializer_class(queryset, many=True).data)

    @action(detail=False, methods=['get'], serializer_class=ServiceRetrieveSerializer)
    def get_service_detail(self, request):
        """
        服务项详情
        """

        try:
            service = self.queryset.get(pk=request.query_params.get('service_id'))
        except Service.DoesNotExist:
            return Response(
                {
                    'result': False,
                    'code': ObjectNotExist.ERROR_CODE_INT,
                    'data': None,
                    'message': ObjectNotExist.MESSAGE,
                }
            )

        return Response(self.serializer_class(service).data)

    @action(detail=False, methods=['get'])
    def get_service_catalogs(self, request):
        """
        服务目录
        """
        has_service = request.query_params.get('has_service')
        service_key = request.query_params.get('service_key')

        # 返回绑定服务项或者根据service_key过滤
        if has_service == 'true' or service_key:
            return Response(ServiceCatalog.open_api_tree_data(service_key=service_key))

        roots = ServiceCatalog.objects.filter(level=0, is_deleted=False)
        return Response([ServiceCatalog.open_api_subtree(root) for root in roots])

    @action(detail=False, methods=['get'])
    def get_service_roles(self, request):
        """
        服务目录
        """
        service_id = request.query_params.get('service_id')
        ticket_creator = request.query_params.get('ticket_creator')
        states = self.queryset.get(id=service_id).workflow.states
        states_roles = []
        for state in states.values():
            if state["processors_type"] == role.OPEN:
                continue

            use_creator = state["processors_type"] in [role.STARTER_LEADER, role.STARTER]
            members = ticket_creator if use_creator else state["processors"]
            if not members:
                processors = ""
            else:
                processors = ",".join(UserRole.get_users_by_type(-1, state["processors_type"], members))
            states_roles.append(
                {
                    "id": state["id"],
                    "name": state["name"],
                    "processors": processors,
                    "processors_type": state["processors_type"],
                    "sign_type": "and" if state["is_multi"] else "or",
                }
            )

        return Response(sorted(states_roles, key=lambda x: x["id"]))

    @action(detail=False, methods=['post'])
    def insert_service(self, requests):
        """
        插入或新服务和流程
        :param requests: 
        :return: 
        """
        services = requests.data.get("services", [])
        flows = requests.data.get("flows", [])
        for new_flow in flows:
            Workflow.objects.restore(data=new_flow)
        if services:
            insert_result = Service.objects.insert_services(services)
            if not insert_result.get("result"):
                raise ServicePartialError(insert_result.get("message"))
        return Response()