'''Testing for ds_messenger'''
import unittest
import ds_messenger


class TestingMessenger(unittest.TestCase):
    '''Test cases for receiving new messages and retrieving all messages'''

    def test_send(self):
        '''Testing for send'''
        server = "168.235.86.101"
        user = "codewars12"
        pw = "hi"
        obj = ds_messenger.DirectMessenger(server, user, pw)
        self.assertEqual(obj.send("hello", "codewars1209"), True)
        server = "this should be wrong"
        obj = ds_messenger.DirectMessenger(server, user, pw)
        self.assertEqual(obj.send("hello", "codewars1209"), False)
        obj = ds_messenger.DirectMessenger()
        self.assertEqual(obj.send("hello", "phonebox711"), False)

    def test_retrieve_new(self):
        '''Testing for retrieve'''
        x = ds_messenger.DirectMessenger("168.235.86.101",
                                         "codewars1209", "hi")
        x.send("this assignment", "codewars12")
        x2 = ds_messenger.DirectMessenger("168.235.86.101",
                                          "codewars12", "hi")
        msgs = x2.retrieve_new()
        self.assertTrue(len(msgs) != 0)
        obj = ds_messenger.DirectMessenger()
        self.assertEqual(obj.retrieve_new(), None)

    def test_retrieve_all(self):
        '''Testing for retrieve all'''
        x2 = ds_messenger.DirectMessenger("168.235.86.101",
                                          "codewars12", "hi")
        allo = x2.retrieve_all()
        self.assertTrue(len(allo) != 0)
        obj = ds_messenger.DirectMessenger()
        self.assertEqual(obj.retrieve_all(), None)


if __name__ == '__main__':
    unittest.main()
