import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from decimal import Decimal

from django.db.models import F
from django.db.models.functions import Mod

from main_app.models import *
from main_app.choices import *


def create_pet(name, species):
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f'{pet.name} is a very cute {pet.species}!'


def create_artifact(name, origin, age, description, is_magical):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f'The artifact {artifact.name} is {artifact.age} years old!'


def rename_artifact(artifact, new_name):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    return '\n'.join(
        f'{location.name} has a population of {location.population}!'
        for location in Location.objects.order_by('-id')
    )


def new_capital():
    Location.objects.filter(
        pk__in=Location.objects.order_by('pk').values_list('pk', flat=True)[:1]
    ).update(is_capital=True)


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()



def first_new_capital():
    Location.objects.filter(
        pk=Location.objects.order_by('pk').values_list('pk', flat=True)[0]
    ).update(is_capital=True)

def second_new_capital():
    Location.objects.filter(
        pk__in=Location.objects.order_by('pk').values_list('pk', flat=True)[:1]
    ).update(is_capital=True)


def apply_discount():
    def update_discount(car):
        car.price_with_discount = car.price * Decimal(1 - sum(int(x) for x in str(car.year)) / 100)
        return car

    Car.objects.bulk_update(
        (update_discount(x) for x in Car.objects.all()),
        ['price_with_discount']
    )

def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    return '\n'.join(
        f'Task - {task.title} needs to be done until {task.due_date}!'
        for task in Task.objects.all()
    )


def complete_odd_tasks():
    Task.objects.annotate(is_odd_id=Mod(F('pk'), 2)).filter(is_odd_id=1).update(is_finished=True)


def encode_and_replace(text: str, task_title: str):
    Task.objects.filter(title=task_title).update(description=''.join(chr(ord(char) - 3) for char in text))


def get_deluxe_rooms():
    return '\n'.join(
        f'Deluxe room with number {room["room_number"]} costs {room["price_per_night"]}$ per night!'
        for room in HotelRoom.objects
        .annotate(is_even_id=Mod(F('pk'), 2))
        .filter(is_even_id=0, room_type=RoomTypeChoices.DELUXE)
        .values('room_number', 'price_per_night')
    )

def increase_room_capacity():
    hotel_rooms = list(HotelRoom.objects.order_by('id'))

    if hotel_rooms[0].is_reserved:
        hotel_rooms[0].capacity += hotel_rooms[0].id

    for i in range(1, len(hotel_rooms)):
        if hotel_rooms[i].is_reserved:
            hotel_rooms[i].capacity += hotel_rooms[i - 1].capacity

    HotelRoom.objects.bulk_update(hotel_rooms, ['capacity'])


def reserve_first_room():
    HotelRoom.objects.filter(
        id__in=HotelRoom.objects.order_by('id').values_list('id', flat=True)[:1]
    ).update(is_reserved=True)


def delete_last_room():
    HotelRoom.objects.filter(
        id__in=HotelRoom.objects.order_by('-id').values_list('id', flat=True)[:1],
        is_reserved=False
    ).delete()


def update_characters():
    Character.objects.filter(class_name=ClassNameChoices.MAGE).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )
    Character.objects.filter(class_name=ClassNameChoices.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )
    Character.objects.filter(class_name__in=(ClassNameChoices.ASSASSIN, ClassNameChoices.SCOUT)).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    if first_character.class_name in (ClassNameChoices.MAGE, ClassNameChoices.SCOUT):
        fusion_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        fusion_inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name='Fusion',
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=first_character.hit_points + second_character.hit_points,
        inventory=fusion_inventory,
    )

    Character.objects.filter(pk__in=(first_character.pk, second_character.pk)).delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()
