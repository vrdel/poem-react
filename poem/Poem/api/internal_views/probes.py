import json

from Poem.api import serializers
from Poem.api.views import NotFound
from Poem.poem_super_admin.models import Probe, ExtRevision

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

import reversion


class ListProbes(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, name=None):
        if name:
            try:
                probe = Probe.objects.get(name=name)
                serializer = serializers.ProbeSerializer(probe)

                return Response(serializer.data)

            except Probe.DoesNotExist:
                raise NotFound(status=404, detail='Probe not found')

        else:
            probes = Probe.objects.all()

            results = []
            for probe in probes:
                # number of probe revisions
                nv = ExtRevision.objects.filter(probeid=probe.id).count()
                results.append(
                    dict(
                        name=probe.name,
                        version=probe.version,
                        docurl=probe.docurl,
                        description=probe.description,
                        comment=probe.comment,
                        repository=probe.repository,
                        nv=nv
                    )
                )

            results = sorted(results, key=lambda k: k['name'].lower())

            return Response(results)

    def put(self, request):
        probe = Probe.objects.get(name=request.data['name'])
        fields = []

        with reversion.create_revision():
            if probe.version != request.data['version']:
                probe.version = request.data['version']
                fields.append('version')

            if probe.repository != request.data['repository']:
                probe.repository = request.data['repository']
                fields.append('repository')

            if probe.docurl != request.data['docurl']:
                probe.docurl = request.data['docurl']
                fields.append('docurl')

            if probe.description != request.data['description']:
                probe.description = request.data['description']
                fields.append('description')

            if probe.comment != request.data['comment']:
                probe.comment = request.data['comment']
                fields.append('comment')

            probe.save()

            reversion.set_user(request.user)
            reversion.set_comment(
                json.dumps(
                    [
                        {
                            'changed': {
                                'fields': fields
                            }
                        }
                    ]
                )
            )

        return Response(status=status.HTTP_201_CREATED)
