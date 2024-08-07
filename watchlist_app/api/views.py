# MY FOLDER
from watchlist_app import models
from watchlist_app.api import serializers, throttling, permissions, pagination

# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets, filters

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
# DJANGO
from django_filters.rest_framework import DjangoFilterBackend

class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

     
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return models.Review.objects.filter(review_user__username=username)



class ReviewCreate(generics.CreateAPIView):
    throttle_classes = [throttling.ReviewCreateThrottle]
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = models.Watchlist.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filterset_fields = ['review_user__username', 'active']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [ScopedRateThrottle]
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_scope = 'review-detail'


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    
class StreamPlatformAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platforms = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            stream_platform = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(stream_platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        stream_platform = models.StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(stream_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        stream_platform = models.StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class WatchlistGV(generics.ListAPIView):
    queryset = models.Watchlist.objects.all()
    serializer_class = serializers.WatchListSerializer
    pagination_class = pagination.WatchListCPagination

class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.Watchlist.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = models.Watchlist.objects.get(pk=pk)
        except models.Watchlist.DoesNotExist:
            return Response({'error':'Movie not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(movie, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = models.Watchlist.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = models.Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)