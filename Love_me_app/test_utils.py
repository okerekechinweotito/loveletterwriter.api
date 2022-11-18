import unittest

from Love_me_app.utils import generate_letter, send_email, send_sms

mock_prompt = "Write a letter to Shade telling her I love her so much in a romantic fashion, from Afeez"

message = generate_letter(mock_prompt)


class MockSender:
    name: str = "Afeez"
    email: str = "lafrizfz@gmail.com"


class MockReciever:
    name: str = "Afeez"
    email: str = "afeezlg@gmail.com"
    phone_number: str = "+2348162302855"


class MockLetter:
    letter: str = message
    reciever = MockReciever
    sender = MockSender


class TestSum(unittest.TestCase):
    def test_letter_generates(self):
        self.assertIsInstance(message, str)

    def test_sending(self):
        send_sms(MockLetter)
        email_response = send_email(MockLetter)
        self.assertEqual(email_response["ResponseMetadata"]["HTTPStatusCode"], 200)


if __name__ == "__main__":
    unittest.main()
