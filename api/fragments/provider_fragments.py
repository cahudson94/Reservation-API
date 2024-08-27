"""."""
import strawberry

from api.scalars.provider_scalar import AddProvider, Provider, ProviderDeleted, ProviderExists


AddProviderResponse = strawberry.union("AddProviderResponse", (Provider, ProviderExists))
DeleteProviderResponse = strawberry.union("DeleteProviderResponse", (Provider, ProviderDeleted))
