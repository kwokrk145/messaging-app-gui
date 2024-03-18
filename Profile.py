# Profile.py
#
# ICS 32
# Assignment #5
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND
# THE JSON SERIALIZATION ASPECTS OF THIS CODE
# RIGHT NOW,
# though can you certainly take a look at it if you are curious since we
# already covered a bit of the JSON format in class.
#
'''Profile Module for creating a profile and
creating, adding, deleting posts'''
import json
import time
from pathlib import Path


class DsuFileError(Exception):
    '''DSUFileError exception'''
    pass


class DsuProfileError(Exception):
    '''DsuProfile Error exception'''
    pass


class Post(dict):
    """

    The Post class is responsible for working
    with individual user posts. It currently
    supports two features: A timestamp property
    that is set upon instantiation and
    when the entry object is set and an entry
    property that stores the post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        '''Set entry'''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        '''Return a specific entry'''
        return self._entry

    def set_time(self, time: float):
        '''Sets time'''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        '''Return timestamp'''
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required
    to join an ICS 32 DSU server. You will need to use
    this class to manage the information provided by
    each new user created within your program for a2.
    Pay close attention to the properties and functions
    in this class as you will need to make use of each of
    them in your program.

    When creating your program you will need to collect
    user input for the properties exposed by this class.
    A Profile class should ensure that a username and password
    are set, but contains no conventions to do so. You
    should make sure that your code verifies that required
    properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL
        self._recipients = []
        self._messages = []

        '''
        add_post accepts a Post object as parameter
        and appends it to the posts list. Posts
        are stored in a list object in the order
        they are added. So if multiple Posts objects
        are created, but added to the Profile in a
        different order, it is possible for the
        list to not be sorted by the Post.timestamp
        property. So take caution as to how you
        implement your add_post code.
        '''

    def add_post(self, post: Post) -> None:
        '''Add post to a profile'''
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        '''Delete post in a profile'''
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        '''Return all posts in a profile'''
        return self._posts
    
    def add_message(self, message):
        self._messages.append(message)
    
    def get_messages(self):
        return self._messages

    def add_friend(self, name):
        self._recipients.append(name)

    def get_friends(self):
        return self._recipients

    def save_profile(self, path: str) -> None:
        '''Save profile information'''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to "
                                   "process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        '''Load exisiting profile information'''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                for name in obj['_recipients']:
                    self._recipients.append(name)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
