import aiohttp
from os import getenv


class SwampApiService:
    """
    A service class for interacting with the SWAMP API.
    """

    async def explain_feed_href(href: str, mode: str = None) -> dict:
        """
        Sends a GET request to the SWAMP API to explain the feed href.

        :param
            href: The href to be explained.
            mode: Explanation mode. Options: 'explain' (default), 'push', 'push_ignore'
        :return: The JSON response from the API.
        """
        if not href:
            raise ValueError("Href cannot be empty.")
        if not isinstance(href, str):
            raise TypeError("Href must be a string.")
        if "http" not in href:
            raise ValueError("Href must be a valid URL.")

        if mode not in [None, 'explain', 'push', 'push_ignore']:
            raise ValueError("Invalid mode. Choose from 'explain', 'push', 'push_ignore'.")

        api_url = f"{getenv('SWAMP_API')}/feeds/parse/?href={href}"
        if mode:
            api_url += f"&mode={mode}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                return await response.json()
