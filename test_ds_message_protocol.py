import unittest
import ds_protocol
import json
class Testing_ds_protocol(unittest.TestCase):
    '''Class for testing server response messages from DSU server'''

    def test_msg_extract(self):
        message = f'{{"response": {{"type": "ok", "message": "Direct message sent"}}}}'
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer.typ, "ok")
        self.assertEqual(answer.msg, "Direct message sent")
        message = f'{{"response": {{"type": "ok", "messages": [{{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"}}, {{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}}]}}}}'
        answer = ds_protocol.directmessage(message, "other")
        self.assertEqual(answer.typ, "ok")
        sent = [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"}, {"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]
        self.assertEqual(answer.msg, sent)
        message = f'{{"response": {{"type": "error", "message": "Direct message sent"}}}}'
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer, None)
        message = "this should result in error"
        answer = ds_protocol.directmessage(message, "direct")
        self.assertEqual(answer, None)

if __name__ == '__main__':
    unittest.main()