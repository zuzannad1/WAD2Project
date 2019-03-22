from selenium.webdriver.common.keys import Keys

def login(self):
    self.browser.get(self.live_server_url + '/admin/')

    # Types username and password
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('testuser')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('test1234')
    password_field.send_keys(Keys.RETURN)

def user_login(self):
    # Types username and password
	username_field = self.browser.find_element_by_name('username')
	username_field.send_keys('testuser')
	
	password_field = self.browser.find_element_by_name('password')
	password_field.send_keys('test1234') 
	password_field.send_keys(Keys.RETURN)

def create_user():
    # Create a user
    from iFood.models import User, UserProfile
    user = User.objects.get_or_create(username="testuser02", first_name="Test",
										last_name="User", email="testuser@testuser.com", password="test1234")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user, address="1234 Test Street",
                                                     facebook="https://facebook.com/facebook-test",
													 twitter="https://twitter.com/twitter-test")[0]
    user_profile.save()

    return user, user_profile
