#This is the function that is first called by AWS, needs to respond
#to the different event types
def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
         return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
         return on_session_ended(event["request"], event["session"])

#Function that is called when a user opens the skill
def on_launch(launch_request, session):
     return get_welcome_response()

#Runs when the skill is trying to use an intent
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "PresentationBriefing":
        return get_presentation()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

#Intent that runs when the user wants to end an interaction
def handle_session_end_request():
    card_title = "The ACM- Thanks!"
    speech_output = "Thank you for coming to the ACM Presenation!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

#Creates the response for when the user opens the skill without a request
def get_welcome_response():
    session_attributes = {}
    should_end_session = False #should this end the interaction?
    card_title = "ACM Alexa Skill Talk" #title that is displayed on Alexa app card
    speech_output = "Welcome to the ACM Tech Talk on Amazon's Alexa! " \
                    "Try asking for a presentation." #Text that Alexa will say
    reprompt_text = "Please ask for a presentation." #If no response is given, Alexa will remind user to say something
    should_end_session = False #Should Alexa keep asking for a response?
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#Generates the response
def get_presentation():
    session_attributes = {}
    card_title = "The ACM- Presentation"
    speech_output = "To hear a presentation on Amazon's Alexa, stay tuned for " \
                    "Pat Cody as he explains how the service works!"

    reprompt_text = "" #if the session is ending, this is unnecessary
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#Generic function to create the speech response (what is actually spoken)
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText", #NOTE: this uses PlainText for simplicity, SSML is also an option
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

#Generic function to build the actual response for Alexa
def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
