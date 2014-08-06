from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from cards.forms import EmailUserCreationForm
from cards.models import Card, Player, WarGame
from cards.test_utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck

__author__ = 'gregorylevin'

from django.test import TestCase

class BasicMathTestCase(TestCase):

    def test_math(self):
        a = 1
        b = 1
        self.assertEqual(a+b, 2)

    # def test_failing_case(self): <--failing test
    #     a = 1
    #     b = 1
    #     self.assertEqual(a+b, 1)

class UtilTestCare(TestCase):
    def test_create_deck_count(self):
        # 'test that we created 52 cards'
        create_deck()
        self.assertEqual(Card.objects.count(), 52)

class ModelTestCase(TestCase):
    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)

    def get_war_result_greater(self):
        user = Card.objects.create(suit=Card.CLUB, rank="jack")
        dealer = Card.objects.create(suit=Card.CLUB, rank="queen")
        self.assertEqual(dealer.get_war_result(user),1)

    def get_war_result_equal(self):
        user = Card.objects.create(suit=Card.CLUB, rank="jack")
        dealer = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(dealer.get_war_result(user), 1)

    def get_war_result_less(self):
        user = Card.objects.create(suit=Card.CLUB, rank="queen")
        dealer = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(dealer.get_war_result(user),1)


class FormTestCase(TestCase):

    def test_clean_username_exception(self):

        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

#error in this function; likely in last line; didn't have time to finish it
    # def test_clean_username(self):
    #     form = EmailUserCreationForm()
    #     form.cleaned_data = {'username':'test-user'}
    #     self.assertAlmostEquals(form, form.cleaned_data)

class ViewTestCase(TestCase):

    def setUp(self):
        create_deck()

# Next, let's write a test for registering for our site. We'll need to make a POST request
# to our register URL, with the appropriate user information. We'll then want to check that
# we've redirected appropriately and that the user was created in the database.

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        self.assertTrue(Player.objects.filter(username=username).exists())

        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

# Let's say you want to test the profile page, but this requires having a user that
# is already logged in. Django's client testing helper, let us login a user then
# perform whatever necessary Django functions we need to do.

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

        # Set up some war game entries
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)

        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertEqual(len(response.context['games']), 2)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn('<p>Suit: spade, Rank: two</p>', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        print response.content

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))


     # def test_login_user(self):
     #
     #     password = 'password'
     #     player = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
     #
     #     data = {
     #         'username': 'test-user',
     #         'password': password,
     #     }
     #    response.self.client.post(reverse('login'), data)
     #    self.assertTrue(player.is_authenticated())
     #    self.assertIsInstance(response, HttpResponseRedirect)
     #    self.assertTrue(response.get('location').endswith(reverse('profile')))






