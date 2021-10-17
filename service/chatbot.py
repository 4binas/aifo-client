from PIL import Image
import os
import urllib.request

class Chatbot:
  def __init__(self, project_id, session_id, language_code, bot_name):
    self.project_id = project_id
    self.session_id = session_id
    self.language_code = language_code
    self.bot_name = bot_name
  
  def __detect_intent_texts__(self, text):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(self.project_id, self.session_id)

    text_input = dialogflow.TextInput(text=text, language_code=self.language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response

  def get_response(self, msg):
    response = self.__detect_intent_texts__(msg)
  
    if len(response.query_result.fulfillment_messages) > 1:
      for message in response.query_result.fulfillment_messages:
        if message.card:
          urllib.request.urlretrieve(
            message.card.image_uri,
            "test")
        
          img = Image.open("test")
          img.show()
          os.remove("test")
    
    return (response.query_result.fulfillment_text or response.query_result.fulfillment_messages[0].text.text[0] or "Sorry, can you repeat that?")