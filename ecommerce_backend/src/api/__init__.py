"""
API package for the e-commerce backend.

Exposes FastAPI app and routers via submodules.
"""
# PUBLIC_INTERFACE
def package_info() -> str:
    """Return brief info about this API package."""
    return "ecommerce_backend.api package containing FastAPI app, routers, models, and utilities."
