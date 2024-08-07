from django.contrib import admin
from .models import Watchlist, StreamPlatform, Review


admin.site.register(Watchlist)
admin.site.register(StreamPlatform)
admin.site.register(Review)