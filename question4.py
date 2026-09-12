# Function Definition


def product_of_multiples(factor, limit):

    # The product starts at 1 because multiplying by 1
    # does not change the result.
    product = 1

    # Generate multiples of factor starting from factor
    # and continuing while the value is less than limit.
    for number in range(factor, limit, factor):

        # Multiply the current product by the multiple.
        product = product * number

    # Return the final product.
    return product


# Example


# Calculate the product of multiples of 3 that are
# less than 10.
result = product_of_multiples(3, 10)

# Display the result.
print(result)



# Expected output:
#
# 162
#
# Explanation:
# The multiples of 3 less than 10 are:
# 3, 6, and 9.
#
# Therefore:
# 3 * 6 * 9 = 162
