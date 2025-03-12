import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from django.db.models import Case, When, Value, CharField, PositiveIntegerField, TextField
from main_app.choices import OperationSystemChoices, BrandChoices, MealTypeChoices, DifficultyChoices, \
    WorkoutTypeChoices


def show_highest_rated_art():
    artwork_gallery = ArtworkGallery.objects.order_by('-rating', 'id').values('art_name', 'rating')[0]
    return f'{artwork_gallery["art_name"]} is the highest-rated art with a {artwork_gallery["rating"]} rating!'


def bulk_create_arts(first_art, second_art):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-id').values('brand', 'price')[0]
    return f'{laptop["brand"]} is the most expensive laptop available for {laptop["price"]}$!'


def bulk_create_laptops(laptops):
    Laptop.objects.bulk_create(laptops)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=[BrandChoices.ASUS, BrandChoices.LENOVO]).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=[BrandChoices.APPLE, BrandChoices.DELL, BrandChoices.ACER]).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand=BrandChoices.ASUS, then=Value(OperationSystemChoices.WINDOWS)),
            When(brand=BrandChoices.APPLE, then=Value(OperationSystemChoices.MACOS)),
            When(brand=BrandChoices.LENOVO, then=Value(OperationSystemChoices.CHROME_OS)),
            When(brand__in=[BrandChoices.DELL, BrandChoices.ACER], then=Value(OperationSystemChoices.LINUX)),
            output_field=CharField()
        ))


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(chess_players):
    ChessPlayer.objects.bulk_create(chess_players)


def delete_chess_players():
    ChessPlayer.objects.filter(title=ChessPlayer._meta.get_field('title').default).delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title=ChessPlayer._meta.get_field('title').default).update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title='FM')


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title='regular player')


def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value('Gordon Ramsay')),
            When(meal_type=MealTypeChoices.LUNCH, then=Value('Julia Child')),
            When(meal_type=MealTypeChoices.DINNER, then=Value('Jamie Oliver')),
            When(meal_type=MealTypeChoices.SNACK, then=Value('Thomas Keller')),
            output_field=CharField()
        ))


def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value('10 minutes')),
            When(meal_type=MealTypeChoices.LUNCH, then=Value('12 minutes')),
            When(meal_type=MealTypeChoices.DINNER, then=Value('15 minutes')),
            When(meal_type=MealTypeChoices.SNACK, then=Value('5 minutes')),
            output_field=CharField()
        ))


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST, MealTypeChoices.DINNER]).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()


def show_hard_dungeons():
    return '\n'.join(
        f'{dungeon["name"]} is guarded by {dungeon["boss_name"]} who has {dungeon["boss_health"]} health points!'
        for dungeon in Dungeon.objects
        .filter(difficulty=DifficultyChoices.HARD)
        .order_by('-location')
        .values('name', 'boss_name', 'boss_health')
    )


def bulk_create_dungeons(dungeons):
    Dungeon.objects.bulk_create(dungeons)

def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
         When(difficulty=DifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DifficultyChoices.HARD, then=Value('The Lost Haunt')),
            output_field=CharField()
        ))


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty=DifficultyChoices.EASY).update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
         When(difficulty=DifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DifficultyChoices.HARD, then=Value(75)),
            output_field=PositiveIntegerField()
        ))


def update_dungeon_rewards():
    Dungeon.objects.update(
        reward=Case(
         When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet')),
            output_field=TextField()
        ))


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
         When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
            output_field=CharField()
        ))


def show_workouts():
    return '\n'.join(
        f'{workout["name"]} from {workout["workout_type"]} type has {workout["difficulty"]} difficulty!'
        for workout in Workout.objects
        .filter(workout_type__in=[WorkoutTypeChoices.CALISTHENICS, WorkoutTypeChoices.CROSSFIT])
        .order_by('id')
        .values('name', 'workout_type', 'difficulty')
    )


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type=WorkoutTypeChoices.CARDIO, difficulty='High').order_by('instructor')


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoices.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value('Chris Heria')),
            output_field=CharField()
        ))


def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
            output_field=CharField()
        ))


def delete_workouts():
    Workout.objects.exclude(workout_type__in=[WorkoutTypeChoices.STRENGTH, WorkoutTypeChoices.CALISTHENICS]).delete()
