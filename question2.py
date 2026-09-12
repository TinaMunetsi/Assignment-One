
from typing import Callable

# Define the class
class EventDispatcher:

    # Initialize the dispatcher
    def __init__(self):
        # Dictionary to store event types and their callbacks
        self._subscribers = {}

    # Register a callback for a specific event type
    def subscribe(self, event_type: str, callback: Callable): 

        # If the event type does not exist, create an empty list
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        # Add the callback to the list
        # Python lists maintain the order in which items are added
        self._subscribers[event_type].append(callback)

    # Remove a registered callback from an event type
    def unsubscribe(self, event_type: str, callback: Callable):

        # Check if the event type exists
        if event_type in self._subscribers:

            # Check if the callback is registered
            if callback in self._subscribers[event_type]:

                # Remove the callback
                self._subscribers[event_type].remove(callback)

            # Remove the event type if there are no callbacks left
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

    # Execute all callbacks registered for an event type
    def dispatch(self, event_type: str, *args, **kwargs):

        # Get the callbacks for the event type
        # Return an empty list if no callbacks are registered
        callbacks = self._subscribers.get(event_type, [])

        # Execute callbacks in registration order
        for callback in callbacks:

            # Handle errors from individual callbacks
            try:

                # Execute the callback and pass the arguments
                callback(*args, **kwargs)

            # Catch exceptions so one callback does not stop the others
            except Exception as error:

                # Print the error message
                print(f"Error in callback: {error}")



# Example usage of the EventDispatcher class


# Create an EventDispatcher object
dispatcher = EventDispatcher()


# Define the first callback function
def callback_one(message):
    print(f"Callback 1 received: {message}")


# Define the second callback function
def callback_two(message):
    print(f"Callback 2 received: {message}")


# Define a callback that will generate an error
def callback_error(message):
    raise Exception("Something went wrong in callback 3")


# Define a fourth callback
def callback_four(message):
    print(f"Callback 4 received: {message}")


# Register the callbacks
# They will execute in this exact order
dispatcher.subscribe("message", callback_one)
dispatcher.subscribe("message", callback_two)
dispatcher.subscribe("message", callback_error)
dispatcher.subscribe("message", callback_four)


# Dispatch the message event
dispatcher.dispatch("message", "Hello World")



# Expected output:
#
# Callback 1 received: Hello World
# Callback 2 received: Hello World
# Error in callback: Something went wrong in callback 3
# Callback 4 received: Hello World
#
# Notice that callback_four still executes even though
# callback_error raised an exception.




# Test unsubscribe()


# Remove callback_two
dispatcher.unsubscribe("message", callback_two)

# Dispatch the event again
# callback_two should no longer execute
dispatcher.dispatch("message", "Second Message")


# Expected output:
#
# Callback 1 received: Second Message
# Error in callback: Something went wrong in callback 3
# Callback 4 received: Second Message