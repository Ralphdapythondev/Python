import random
import string
import logging
import argparse
from urllib.parse import urlparse, urlunparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_random_tld(common_tlds=None):
    """
    Generates a random top-level domain.

    Parameters:
        common_tlds (list of str, optional): A list of common TLDs to choose from.
            Defaults to ['com', 'net', 'org', 'info', 'biz', 'co', 'us', 'uk'].

    Returns:
        str: A randomly generated TLD (e.g., 'com', 'org', 'xyz').
    """
    if common_tlds is None:
        common_tlds = ['com', 'net', 'org', 'info', 'biz', 'co', 'us', 'uk']

    tld = random.choice(common_tlds) if random.choice([True, False]) else ''.join(
        random.choices(string.ascii_lowercase, k=random.choice([2, 3]))
    )

    logging.debug(f"Generated TLD: {tld}")
    return tld


def generate_links(base_url, num_links=10, path_pattern="/page{}"):
    """
    Generates a list of URLs based on a base URL with random paths and TLDs.

    Parameters:
        base_url (str): The base URL to use as a template (e.g., 'https://example.com').
        num_links (int): The number of links to generate.
        path_pattern (str): The pattern for generating paths. Defaults to "/page{}".

    Returns:
        list of str: A list of generated URLs.
    """
    try:
        parsed_url = urlparse(base_url)
    except ValueError as e:
        logging.error(f"Invalid base URL: {base_url}")
        raise ValueError(f"Invalid base URL: {base_url}") from e

    base_hostname = parsed_url.hostname.split('.')[0]
    generated_links = []

    for i in range(1, num_links + 1):
        path = path_pattern.format(i)
        random_tld = generate_random_tld()
        new_hostname = f"{base_hostname}.{random_tld}"
        new_url = parsed_url._replace(netloc=new_hostname, path=path)
        generated_links.append(urlunparse(new_url))

    logging.info(f"Generated {len(generated_links)} links based on {base_url}")
    return generated_links


def randomize_and_generate_links(base_url, num_links=10, path_pattern="/page{}"):
    """
    Generates and randomizes a list of URLs based on a base URL.

    Parameters:
        base_url (str): The base URL to use as a template (e.g., 'https://example.com').
        num_links (int): The number of links to generate.
        path_pattern (str): The pattern for generating paths. Defaults to "/page{}".

    Returns:
        list of str: A list of randomized and generated URLs.
    """
    generated_links = generate_links(base_url, num_links, path_pattern)
    random.shuffle(generated_links)
    logging.info("Randomized the order of generated links.")
    return generated_links


def main():
    parser = argparse.ArgumentParser(
        description="Generate and randomize URLs based on a base URL."
    )
    parser.add_argument(
        'base_url', type=str, help="The base URL to use (e.g., 'https://example.com')."
    )
    parser.add_argument(
        '--num-links', type=int, default=10,
        help="The number of links to generate (default: 10)."
    )
    parser.add_argument(
        '--path-pattern', type=str, default="/page{}",
        help="The pattern for generating paths (default: '/page{}')."
    )
    args = parser.parse_args()

    randomized_links = randomize_and_generate_links(
        args.base_url, args.num_links, args.path_pattern
    )
    print("Randomized and Generated Links:")
    for link in randomized_links:
        print(link)


if __name__ == "__main__":
    main()
