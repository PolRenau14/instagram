from time import sleep
import random
import instaloader
from selenium import webdriver
import json
import os.path
import os

# Required Env variables for login, It can be defined here.
usr = os.getenv("INSTA_USR", "DEFAULT")
psw = os.getenv("INSTA_PSW", "DEFAULT")


class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

    def go_to_login_page(self):
        return PageManager(self.browser)


class PageManager:
    def __init__(self, browser):
        self.browser = browser
        self.followers = []

    def login(self, username, password):
        # Get followers from instagram
        if not os.path.isfile("followers.json"):
            L = instaloader.Instaloader()
            # Login or load session
            L.login(username, password)  # (login)
            # Obtain profile metadata
            profile = instaloader.Profile.from_username(L.context, username)
            self.followers = profile.get_followers()
            self.followers = [x.username for x in self.followers]
            with open('followers.json', 'w') as json_file:
                json.dump(self.followers, json_file)
        # Read list of followers, you can use as list of persons that you want to mention
        else:
            with open('followers.json') as f:
                self.followers = json.load(f)

        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        sleep(2)

    def click_button(self, text):
        button = self.browser.find_element_by_xpath("//button[text()='{}']".format(text))
        button.click()

    def search_objective(self, usr):
        self.browser.get('https://www.instagram.com/{}/'.format(usr))

    def comment_all_pubs_from_perf(self, comments:list):
        len_max = len(comments) -1

        num_pubs = int(self.browser.find_element_by_class_name('g47SY ').text)
        self.browser.find_element_by_class_name('v1Nh3').click()
        i = 1
        while i <= num_pubs:
            comment_bar = self.browser.find_element_by_class_name('Ypffh')
            comment_bar.click()

            comment_bar = self.browser.find_element_by_class_name('Ypffh')
            random_comment = random.randint(0, len_max)
            comment_bar.send_keys(comments[random_comment])
            self.click_button("Post")
            sleep(30)
            self.browser.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
            i += 1

    def massive_comment_to_publi(self, url, usrs_per_publi):
        self.search_objective(url)
        max_publis_day = 180
        # To evit that instagram banns you this split the max publications that you can make on one day
        sleep_time = (60*60*24)/max_publis_day
        num_comments = int(len(self.followers)/usrs_per_publi)
        # If followers commented doesn't exists
        commented = []
        if os.path.isfile("commented.json.json"):
            with open('commented.json') as f:
                commented = json.load(f)

        for i in range(num_comments):
            try:
                if self.followers[i*usrs_per_publi] not in commented:
                    comment = ""
                    for j in range(usrs_per_publi):
                        commented.append(self.followers[i*usrs_per_publi+j])
                        comment += "@{} ".format(self.followers[i*usrs_per_publi+j])
                        print(comment)
                    comment_bar = self.browser.find_element_by_class_name('Ypffh')
                    comment_bar.click()

                    comment_bar = self.browser.find_element_by_class_name('Ypffh')
                    comment_bar.send_keys(comment)
                    self.click_button("Post")
                    with open('commented.json', 'w') as json_file:
                        json.dump(commented, json_file)
                    sleep(sleep_time)
            except:
                print("Can't comment for user {}".format(self.followers[i*usrs_per_publi]))
                pass


if __name__ == "__main__":

    if usr == "DEFAULT" or psw == "DEFAULT":
        raise Exception("You should define env variables: INSTA_USR, INSTA_PSW")

    browser = webdriver.Firefox()
    browser.implicitly_wait(5)

    home_page = HomePage(browser)
    login_page = home_page.go_to_login_page()

    # Sometimes appear pop_up to accept Cookies but not always
    try:
        sleep(3)
        login_page.click_button("Accept")
    except:
        pass

    login_page.login(usr, psw)

    login_page.click_button("Not Now")
    login_page.click_button("Not Now")

    # Rename_for more understand code.
    instagram_manager = login_page

    # Change this parameters depending on publication conditions
    publi_url = "p/CIVv9jCJA3n"
    participants_coment = 1
    instagram_manager.massive_comment_to_publi(publi_url, participants_coment)
