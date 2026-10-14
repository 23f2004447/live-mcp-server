import hashlib
import os

import uvicorn
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "23f2004447@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "exam-server",
    stateless_http=True,      # every request stands alone (no sessions to lose)
    json_response=True,       # plain JSON replies
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Reads the exam challenge from the HTTP headers and returns the answer."""
    headers = ctx.request_context.request.headers      # the HTTP headers of THIS call
    challenge = headers.get("x-exam-challenge", "")
    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()
    return digest[:16]


app = mcp.streamable_http_app()       # the endpoint will be  https://<your-host>/mcp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
