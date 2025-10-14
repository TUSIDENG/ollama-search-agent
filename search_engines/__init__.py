# search_engines/__init__.py
from .base_search import BaseSearch
from .placeholder_search import PlaceholderSearch
from .brave_search import BraveSearch
from .google_search import GoogleSearch
from .bing_search import BingSearch
from .custom_google_search import CustomGoogleSearch, CustomGoogleSearchAPIWrapper
from .factory import (
    SearchEngineFactory,
    create_search_engine,
    get_default_search_engine,
    list_available_engines,
    check_engine_availability,
    register_search_engine,
    get_engine_info
)
