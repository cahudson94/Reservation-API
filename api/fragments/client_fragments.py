"""."""

import strawberry

from api.scalars.client_scalar import (
    AddClient,
    ClientDeleted,
    ClientNotFound,
    ClientExists,
    ClientIdMissing,
)


AddClientResponse = strawberry.union("AddClientResponse", (AddClient, ClientExists))
DeleteClientResponse = strawberry.union(
    "DeleteClientResponse", (ClientDeleted, ClientNotFound, ClientIdMissing)
)
