"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}

def create_output(sentence, intent, session):
    # This function makes sentence the output of Alexa
    card_title = intent['name']
    session_attributes = session['attributes']
    should_end_session = False

    speech_output = sentence
    reprompt_text = sentence

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def create_cpr_output(intent, session):
    response = ""
    if session['attributes']['compressions']:
        response += "Perform 30 press compressions. "
        if session['attributes']['cpr_first']:
            response += cpr_instructions('compressions')
    else:
        response += "Give 2 rescue breaths. "
        if session['attributes']['cpr_first']:
            response += cpr_instructions('breaths')

    response += "To begin say 'Ready'. "
    return create_output(response, intent, session)

def cpr_instructions(ins_type):
    if ins_type == 'compressions':
        return "Instructions: Person must be on a firm, flat surface. Push hard, push fast in the middle of the chest at least 2 inches deep and at least 100 compressions per minute. "
    elif ins_type == 'breaths':
        return "Instructions: Tilt the head up and lift the chin up. Pinch the nose shut then make a complete seal over the person's mouth. Blow in for about 1 second to make the chest clearly rise. Give the rescue breaths one after the other. If chest doesn't raise with rescue breaths, retilt the head and give another rescue breath. "
    else:
        return     

def cpr_help(intent, session):
    """
    Things you need to keep track of:
        Is this the first iteration?
        Place in the iteration

    """
    response = ""
    if 'cpr' in session['attributes']:
        if 'Stage' in intent['slots'].keys():
            # can be question
            value = intent['slots']['Stage']['value']
            if value == 'compressions':
                return create_output(cpr_instructions('compressions'), intent, session)
            elif value == 'breaths':
                return create_output(cpr_instructions('breaths'), intent, session)
            elif value == 'ready':
                response += "When you are done, say done. "
                return create_output(response, intent, session)
            elif value == 'done':
                if session['attributes']['compressions']:
                    # compressions are done
                    session['attributes']['compressions'] = False
                    return create_cpr_output(intent, session)
                else:
                    session['attributes']['compressions'] = True
                    session['attributes']['cpr_first'] = False
                    return create_cpr_output(intent, session)
            elif value == 'stop':
                session['attributes']={}
                return create_output("", intent, session)


    else:
        session['attributes']['cpr'] = True
        session['attributes']['compressions'] = True
        session['attributes']['cpr_first'] = True
        return create_cpr_output(intent, session)

    # if 'cpr' in problem:
    #     #Perform CPR
    #     return create_output('sjldfhalksdjfhlka', intent, session)


        
        # Respond at any time: how do I do compressions/breaths
        # "Restart XX" takes you to XX
        # If user says "stop cpr" or "quit cpr" exit loop

        # Begin chest compressions: perform 30 chest compressions
        # if this is first time - explain compressions

        #when youre ready say ready
        #when youre done say done

        # Begin rescue breaths: now give the the user two rescue breaths
        #if this is the first time - explain rescue breaths

        #when youre ready say ready
        #when youre done say done

        # loop

def get_help(intent, session):

    problem = intent['slots']['Problem']['value']

    if 'cpr' in problem:
        return cpr_help(intent, session)

    elif ('choking' in problem) or 'choking' in session['attributes']:
        if 'unconcious' in problem:
            return call_911(intent, session)
        elif 'concious' in problem:
            return call_911(intent, session)
        else:
            #ask what kind
            
            card_title = intent['name']
            session_attributes = {"choking":True}
            should_end_session = False

            speech_output = ""
            reprompt_text = "Is the victim concious or unconcious?"

            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    elif (('injured' in problem) or ('aed' in problem) or ('bleeding' in problem) or ('burn' in problem) or ('poison' in problem) or ('neck' in problem) or ('spinal' in problem) or ('stroke' in problem)):
        return call_911(intent, session)
    else:
        speech_output = "I'm not sure I understand what you need help with. "\
                    "You can say 'Help me with': "\
                    "Checking an injured adult, choking, CPR, AED, controlling bleeding, " \
                    "Burns, Poisoning, Neck injuries, spinal injuries or strokes."
        return create_output(speech_output, intent, session)           

    return call_911(intent, session)

def call_911(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Call 911."
    reprompt_text = "Call 911."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def what_can_I_say(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "You can say 'Help me with': "\
                    "Checking an injured adult, choking, CPR, AED, controlling bleeding, " \
                    "Burns, Poisoning, Neck injuries, spinal injuries or strokes."
    reprompt_text = "I'm not sure I understand what you need help with. "\
                    "You can say 'Help me with': "\
                    "Checking an injured adult, choking, CPR, AED, controlling bleeding, " \
                    "Burns, Poisoning, Neck injuries, spinal injuries or strokes."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "CPR":
        return cpr_help(intent, session)
    elif intent_name == "NeedHelp":
        return get_help(intent, session)
    elif intent_name == "WhatCanISay":
        return what_can_I_say(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
