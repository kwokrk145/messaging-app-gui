'''Test cases for ds_protocol'''
import unittest
import ds_protocol


class TestingProtocol(unittest.TestCase):
    '''Class for testing server response messages from DSU server'''

    def test_msg_extract(self):
        '''Testing message extract'''
        y = "ok"
        message = f'{{"response": {{"type": "{y}", \
                    "message": "Direct message sent"}}}}'
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer.typ, "ok")
        self.assertEqual(answer.msg, "Direct message sent")
        x = "Hello User 1!"
        message = f'{{"response": {{"type": "ok", "messages": \
                    [{{"message":"{x}", "from":"markb", \
                    "timestamp":"1603167689.3928561"}}, \
                    {{"message":"Bzzzzz", "from":"thebeemoviescript", \
                    "timestamp":"1603167689.3928561"}}]}}}}'
        answer = ds_protocol.directmessage(message, "other")
        self.assertEqual(answer.typ, "ok")
        sent = [{"message": "Hello User 1!", "from": "markb",
                "timestamp": "1603167689.3928561"},
                {"message": "Bzzzzz", "from": "thebeemoviescript",
                "timestamp": "1603167689.3928561"}]
        self.assertEqual(answer.msg, sent)
        z = "error"
        message = f'{{"response": {{"type": "{z}", \
                    "message": "Direct message sent"}}}}'
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer, None)
        message = "this should result in error"
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer, None)


if __name__ == '__main__':
    unittest.main()
