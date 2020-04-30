

from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from commodities.models import HsChapter, HsHeading, HsSubheading
from commodities.serializers import hs as serializers



class GetHsItemView(views.APIView):

    def get(self, request, code):

        if len(code) == 2:
            level, model = 'chapter', HsChapter
        elif len(code) == 4:
            level, model = 'heading', HsHeading
        elif len(code) == 6:
            level, model = 'subheading', HsSubheading
        else:
            return Response({
                'error': 'invalid_code',
                'message': 'Expected a 2, 4 or 6 digit Harmonized System code.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = model.objects.get(code=code)
        except model.DoesNotExist:
            return Response({
                'error': 'code_not_found',
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'code': code,
            'description': item.description,
            'level': level
        }, status=status.HTTP_200_OK)

