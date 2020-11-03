# -*- coding: utf-8 -*-

import json
import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler,
                                              AbstractRequestInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response

import prompts
from jentris import Jentris

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

local_replies = None


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Create output speech
        speak_output = data[prompts.WELCOME]

        return (
            handler_input.response_builder.speak(speak_output).ask(speak_output).response
        )


class DaysUntilJentrisIntentHandler(AbstractRequestHandler):
    """Handler for Days Until Jentris Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DaysUntilJentrisIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Get Jentris data - got to calculate this each time an intent is invoked
        jentris = Jentris()

        # If something has gone wrong, let the user know
        if jentris.error:
            speak_output = data[prompts.ERROR]
        else:
            # Successfully computed data, so go ahead and inform the user
            # print(f"Next J Day: {jentris.jentris_date}")
            # print(f"Sleeps until J Day: {jentris.jentris_sleeps}")
            # print(f"Date in text: {jentris.jentris_date_text}")

            # Create output speech
            # If today is J-Day, let it be known!
            if jentris.is_j_today:
                speak_output = f"{data[prompts.J_DAY]}"
            else:
                speak_output = f"{data[prompts.THERE_ARE]} {jentris.jentris_sleeps} {data[prompts.SLEEPS_UNTIL]}"
        return (
            handler_input.response_builder.speak(speak_output).response
        )


class NextJentrisIntentHandler(AbstractRequestHandler):
    """Handler for Next Jentris Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NextJentrisIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Get Jentris data - got to calculate this each time an intent is invoked
        jentris = Jentris()

        # If something has gone wrong, let the user know
        if jentris.error:
            speak_output = data[prompts.ERROR]
        else:
            # Successfully computed data, so go ahead and inform the user
            # print(f"Next J Day: {jentris.jentris_date}")
            # print(f"Sleeps until J Day: {jentris.jentris_sleeps}")
            # print(f"Date in text: {jentris.jentris_date_text}")
            # If today is J-Day, let it be known!
            if jentris.is_j_today:
                speak_output = f"{data[prompts.J_DAY]}"
            else:
                speak_output = f"{data[prompts.JENTRIS_IS_ON]} {jentris.jentris_date_text}"

        return (
            handler_input.response_builder.speak(speak_output).response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Speak the help prompt
        speak_output = data[prompts.HELP]

        return (
            handler_input.response_builder.speak(speak_output).ask(speak_output).response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Say Goodbye
        speak_output = data[prompts.GOODBYE]

        return (
            handler_input.response_builder.speak(speak_output).response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder.speak(speak_output).response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale[:2]))

        # Localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)

        # Set default translation data to broader translation
        data = language_data[locale[:2]]
        # If a more specialized translation exists, then select it instead
        # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
        #          then pick that instead
        if locale in language_data:
            data.update(language_data[locale])
        handler_input.attributes_manager.request_attributes["_"] = data


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        # Get localised strings
        data = handler_input.attributes_manager.request_attributes["_"]

        # Speak the help prompt
        speak_output = data[prompts.ERROR]

        return (
            handler_input.response_builder.speak(speak_output).ask(speak_output).response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DaysUntilJentrisIntentHandler())
sb.add_request_handler(NextJentrisIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler()
)  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
