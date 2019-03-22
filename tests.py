# Imports
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.template import loader
from django.conf import settings
from iFood.models import User, UserProfile
from iFood.forms import UserForm, UserProfileForm
from selenium.webdriver.common.keys import Keys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
import test_utils
import os, socket
import os.path

# Test cases

class TemplateTests(TestCase):
              
	def test_index_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('index'))
		self.assertTemplateUsed(response, 'ifood/base.html')
	
	def test_about_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('about'))
		self.assertTemplateUsed(response, 'ifood/base.html')
		
	def test_contact_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('contact'))
		self.assertTemplateUsed(response, 'ifood/base.html')
		
	def test_login_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('login'))
		self.assertTemplateUsed(response, 'ifood/base.html')

	def test_signup_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('signup'))
		self.assertTemplateUsed(response, 'iFood/base.html')
		
	def test_account_using_template(self):
		# Check the template base is being used
		response = self.client.get(reverse('account'))
		self.assertTemplateNotUsed(response, 'ifood/account.html')
		
class UserAuthenticationTests(StaticLiveServerTestCase):
	
	def setUp(self):
		from django.contrib.auth.models import User
		User.objects.create_superuser(username='testuser', password='test1234', email='testuser@testuser.com')
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('headless')
		self.browser = webdriver.Chrome(chrome_options = chrome_options)
		self.browser.implicitly_wait(3)

	@classmethod
	def setUpClass(cls):
		cls.host = socket.gethostbyname(socket.gethostname())
		super(UserAuthenticationTests, cls).setUpClass()

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()
	
	def test_register_user(self):
		# Check if register works
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')

		try:
			self.browser.get(url + reverse('index'))
		except:
			try:
				self.browser.get(url + reverse('iFood:index'))
			except:
				return False
		
		#Click in Register
		self.browser.find_elements_by_link_text('Sign Up')[0].click()

		# Fill registration form
		# username
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testuser03')
		
		# first name
		username_field = self.browser.find_element_by_name('first_name')
		username_field.send_keys('Test')
		
		# last name
		username_field = self.browser.find_element_by_name('last_name')
		username_field.send_keys('User')

		# email
		email_field = self.browser.find_element_by_name('email')
		email_field.send_keys('testuser@testuser.com')

		# password
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('test1234')

		# address
		address_field = self.browser.find_element_by_name('address')
		address_field.send_keys('1234 Test Street')
		
		# facebook
		facebook_field = self.browser.find_element_by_name('facebook')
		facebook_field.send_keys('https://facebook.com/facebook-test')
		
		# twitter
		twitter_field = self.browser.find_element_by_name('twitter')
		twitter_field.send_keys('https://twitter.com/twitter-test')

		# Submit
		twitter_field.send_keys(Keys.RETURN)

		body = self.browser.find_element_by_tag_name('body')

		# Check for success message
		self.assertIn('Thank you for registering!'.lower(), body.text.lower())
		self.browser.find_element_by_class_name('logo')
	
	def test_links_in_index_page_when_logged(self):
		# Access login page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('login'))
		except:
			try:
				self.browser.get(url + reverse('iFood:login'))
			except:
				return False

		# Log in
		test_utils.user_login(self)

		#Check links that appear for logged person only
		self.browser.find_element_by_link_text('testuser')
		self.browser.find_element_by_link_text('Log Out')

		# Check that links does not appears for logged users
		body = self.browser.find_element_by_tag_name('body')
		self.assertNotIn('Sign In', body.text)
		self.assertNotIn('Sign Up', body.text)
		
	def test_links_in_index_page_when_not_logged(self):
		#Access index page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('index'))
		except:
			try:
				self.browser.get(url + reverse('iFood:index'))
			except:
				return False

		#Check links that appear for not logged person only
		self.browser.find_element_by_link_text('Sign In')
		self.browser.find_element_by_link_text('Sign Up')

		# Check that links does not appears for not logged users
		body = self.browser.find_element_by_tag_name('body')
		self.assertNotIn('testuser', body.text)
		self.assertNotIn('Sign Out', body.text)

	def test_logout_link(self):
		# Access login page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('login'))
		except:
			try:
				self.browser.get(url + reverse('iFood:login'))
			except:
				return False
		
		# Fill login form
		test_utils.user_login(self)

		#Clicks to logout
		self.browser.find_element_by_link_text('Log Out').click()

		# Check if it see log in link, thus it is logged out
		self.browser.find_element_by_link_text('Sign In')
		
	def test_account_appears_when_logged(self):
		# Access login page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('login'))
		except:
			try:
				self.browser.get(url + reverse('iFood:login'))
			except:
				return False

		# Log in
		test_utils.user_login(self)

		# Check if account appears
		self.browser.find_element_by_link_text('testuser')

	def test_account_page_when_not_logged(self):
		# Access account page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('account'))
		except:
			try:
				self.browser.get(url + reverse('iFood:account'))
			except:
				return False

		# Check login form is displayed
		# username
		self.browser.find_element_by_name('username')

		# password
		self.browser.find_element_by_name('password')

	def test_logged_user_message_in_index(self):
		# Access login page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('login'))
		except:
			try:
				self.browser.get(url + reverse('iFood:login'))
			except:
				return False

		# Log in
		test_utils.user_login(self)

		# Check for the username in the message
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('testuser', body.text)

	def test_login_provides_error_message(self):
		# Access login page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('login'))
		except:
			try:
				self.browser.get(url + reverse('iFood:login'))
			except:
				return False
				
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('wronguser')
	
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('wrongpass') 
		password_field.send_keys(Keys.RETURN)
			
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Invalid login details supplied.', body.text)

	def test_login_redirects_to_index(self):
		# Access login page via POST with user data
		try:
			response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'test1234'})
		except:
			try:
				response = self.client.post(reverse('iFood:login'), {'username': 'testuser', 'password': 'test1234'})
			except:
				return False

		# Check it redirects to index
		self.assertRedirects(response, reverse('index'))
		
	def test_cart_when_not_logged(self):
		# Access cart page
		url = self.live_server_url
		url = url.replace('localhost', '127.0.0.1')
		try:
			self.browser.get(url + reverse('cart'))
		except:
			try:
				self.browser.get(url + reverse('iFood:cart'))
			except:
				return False
		
		# Check it redirects to login
		# username
		self.browser.find_element_by_name('username')

		# password
		self.browser.find_element_by_name('password')