import random
import string

def generate_random_string(n):
    """Generates a random string of length n."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
