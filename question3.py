# Typed Data Descriptor


class Typed:

    # Initialize the descriptor with the expected type
    def __init__(self, expected_type):
        self.expected_type = expected_type

        # Store the name that will be used for the actual
        # value on the instance.
        # An empty string avoids Pylance type warnings.
        self.storage_name: str = ""

    # Automatically receives the attribute name when the
    # descriptor is assigned to a class attribute.
    def __set_name__(self, owner, name):

        # Create a private storage attribute name.
        # For example, age becomes _age.
        self.storage_name = "_" + name

    # Retrieve the value from the instance
    def __get__(self, instance, owner):

        # If accessed through the class rather than an instance,
        # return the descriptor itself.
        if instance is None:
            return self

        # Return the value stored in the private attribute.
        return getattr(instance, self.storage_name, None)

    # Control assignment to the managed attribute
    def __set__(self, instance, value):

        # Check whether the assigned value has the expected type.
        if not isinstance(value, self.expected_type):

            # Raise the required TypeError message.
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

        # Store the valid value using the automatically
        # generated storage attribute name.
        setattr(instance, self.storage_name, value)


# Example class using the Typed descriptor


class Person:

    # age must be an integer
    age = Typed(int)

    # name must be a string
    name = Typed(str)


# Create a Person object


person = Person()


# Valid assignments


# Assign an integer to age
person.age = 25

# Assign a string to name
person.name = "John"


# Display the values

print(person.age)
print(person.name)


# Invalid assignment


# This will raise:
# TypeError: Expected int, got str

person.age = "25"


# This will raise:
# TypeError: Expected str, got int

person.name = 100
