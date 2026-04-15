import unittest
from unittest.mock import patch, MagicMock
import json
from logic import process_user_intent
import os

class TestLogic(unittest.TestCase):
    
    @patch('logic.genai.Client')
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    def test_process_user_intent_meeting(self, mock_client_class):
        # Arrange
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        expected_json = {
            "intent": "meeting_scheduling",
            "client_name": "Acme Corp",
            "client_email": "hello@acme.com",
            "start_time": "2023-11-20T10:00:00.000000",
            "end_time": "2023-11-20T11:00:00.000000",
            "task_description": "Prepare slides for Acme Corp"
        }
        
        mock_response = MagicMock()
        mock_response.text = json.dumps(expected_json)
        mock_client_instance.models.generate_content.return_value = mock_response

        # Act
        result = process_user_intent("Acme Corp wants to meet on Nov 20th at 10am.")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.get("intent"), "meeting_scheduling")
        self.assertEqual(result.get("client_name"), "Acme Corp")
        
    @patch('logic.genai.Client')
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    def test_process_user_intent_invalid_json(self, mock_client_class):
        # Arrange
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        mock_response = MagicMock()
        mock_response.text = "This is not valid json"
        mock_client_instance.models.generate_content.return_value = mock_response

        # Act
        result = process_user_intent("A confusing query.")

        # Assert
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
