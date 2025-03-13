import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, Registration
from django.db.models import Avg
from datetime import timedelta, date


def show_all_authors_with_their_books():
    return '\n'.join(
        f'{author.name} has written - {", ".join(book.title for book in author.book_set.all())}!'
        for author in Author.objects
        .prefetch_related('book_set')
        .order_by('id')
        if author.book_set.exists()
    )


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name):
    return Artist.objects.get(name=artist_name).songs.order_by('-id')


def remove_song_from_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name):
    return (
        Product.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .filter(name=product_name)
        .values_list('avg_rating', flat=True )
        .first()
    )



def get_reviews_with_high_ratings(threshold):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    return '\n'.join(
        f'License with number: {lic["license_number"]} expires on {lic["issue_date"] + timedelta(days=365)}!'
        for lic in DrivingLicense.objects
        .order_by('-license_number')
        .values('license_number', 'issue_date')
    )


def get_drivers_with_expired_licenses(due_date):
    return Driver.objects.filter(license__issue_date__lt=due_date - timedelta(days=365))


def register_car_by_owner(owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(owner__isnull=True).first()

    car.owner = owner
    car.save()

    registration.car = car
    registration.registration_date = date.today()
    registration.save()

    return (
        f'Successfully registered {car.model} to {owner.name} with registration number '
        f'{registration.registration_number}.'
    )
