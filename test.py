from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # def setUp(self):
    #     """ before each test"""

    #     app.config['TESTING'] = True  #?

    def test_show_board(self):
        """test if the html displays and informations stored in session"""

        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)       
            self.assertIn('Your highest score is', html)
            self.assertIn('Start', html)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))


    def test_valid_word(self):
        """ test check the valid word"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["S", "X", "X", "X", "X"],
                                           ["I", "X", "X", "X", "X"],
                                           ["X", "X", "X", "X", "X"],
                                           ["X", "X", "X", "X", "X"],
                                           ["X", "X", "X", "X", "X"]]
            # indentation!!!!!
            response = client.get("/check-word?word=six")            
            self.assertEqual(response.status_code, 200)
            # self.assertEqual(response.data.result, "ok")  // not working
            self.assertEqual(response.json['result'], 'ok')
            # self.assertEqual(response.get_json()['result'], 'ok') also work

           
    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        with app.test_client() as client:
            client.get('/')
            # this test uses the real board?
            # hwo can we guarantee no "impossible" on the board?
            response = client.get('/check-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')


    def non_english_word(self):
        """Test if word is on the board"""

        with app.test_client() as client: 
            client.get('/')
            response = client.get(
                '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
            self.assertEqual(response.json['result'], 'not-word')
