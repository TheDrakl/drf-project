from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListAV, WatchDetailAV,
                                      StreamPlatformAV, StreamPlatformDetailAV,
                                      StreamPlatformVS, 
                                      ReviewList, ReviewDetail, ReviewCreate,
                                      UserReview, WatchlistGV
)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist-list'),
    path('list2/', WatchlistGV.as_view(), name='watchlist-list-2'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watchlist-detail'),
    #path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    #path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('', include(router.urls)),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReview.as_view(), name='review-user'),
]
