# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

# Django
from django.db.models import (
    Avg,
    Count,
    Max,
    Min,
)

# Third Party
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# wger
from wger.weight.api.filtersets import WeightEntryFilterSet
from wger.weight.api.serializers import WeightEntrySerializer
from wger.weight.models import WeightEntry


class WeightEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for weight entry objects
    """

    serializer_class = WeightEntrySerializer

    is_private = True
    ordering_fields = '__all__'
    filterset_class = WeightEntryFilterSet

    def get_queryset(self):
        """
        Only allow access to appropriate objects
        """
        # REST API generation
        if getattr(self, 'swagger_fake_view', False):
            return WeightEntry.objects.none()

        return WeightEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the owner
        """
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'user',
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=(
                    'ID of the user whose summary to return. Used by the gym trainer '
                    'view. Defaults to the logged in user.'
                ),
            ),
        ],
    )
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns aggregate statistics for a user's weight entries:
        count, min_weight, max_weight, avg_weight.

        Trainers open this for the members they manage, so the user can be given
        explicitly with ?user=. Without it the logged in user's own entries are
        summarised.
        """
        user_id = request.query_params.get('user')
        if user_id:
            qs = WeightEntry.objects.filter(user_id=user_id)
        else:
            qs = self.get_queryset()

        stats = qs.aggregate(
            count=Count('id'),
            min_weight=Min('weight'),
            max_weight=Max('weight'),
            avg_weight=Avg('weight'),
        )
        return Response(stats)
