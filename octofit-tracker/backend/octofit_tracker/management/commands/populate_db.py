from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Smazat stará data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Týmy
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Uživatelé
        users = [
            User.objects.create(email='ironman@marvel.com', name='Iron Man', team='marvel'),
            User.objects.create(email='spiderman@marvel.com', name='Spider-Man', team='marvel'),
            User.objects.create(email='batman@dc.com', name='Batman', team='dc'),
            User.objects.create(email='superman@dc.com', name='Superman', team='dc'),
        ]

        # Aktivity
        Activity.objects.create(user='ironman@marvel.com', activity_type='run', duration=30, date='2024-01-01')
        Activity.objects.create(user='spiderman@marvel.com', activity_type='swim', duration=45, date='2024-01-02')
        Activity.objects.create(user='batman@dc.com', activity_type='cycle', duration=60, date='2024-01-03')
        Activity.objects.create(user='superman@dc.com', activity_type='fly', duration=120, date='2024-01-04')

        # Leaderboard
        Leaderboard.objects.create(team='marvel', points=150)
        Leaderboard.objects.create(team='dc', points=180)

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Situps', description='Do 30 situps', difficulty='medium')
        Workout.objects.create(name='Plank', description='Hold plank for 1 min', difficulty='hard')

        # Unikátní index na email v users
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.user.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Test data successfully populated in octofit_db!'))
