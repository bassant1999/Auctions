from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:lid>/<int:uid>", views.comment, name="comment"),
    path("listing/bid/<int:lid>/<int:uid>", views.bid, name="bid"),
    path("user/<int:uid>", views.viewProfile, name="profile"),
    path("add/<int:uid>", views.create_listing, name="add"),
    path("watchlist/<int:uid>/<int:lid>", views.addToWatchlist, name="watchlist"),
    path("watchlist/<int:uid>", views.watchlist, name="showwatchlist"),
    path("inactivate/<int:uid>/<int:lid>", views.inactivate, name="inactivate"),
    path("notify/<int:uid>", views.notify, name="notify"),
    path("remove/<int:lid>/<int:uid>", views.remove, name="remove"),
]

### New ####
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

