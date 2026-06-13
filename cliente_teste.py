import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def parse_content(result):
    """Extrai e parseia o conteúdo do resultado de uma tool call."""
    content = result.content
    if not content:
        raise ValueError("Conteúdo vazio na resposta da tool")
    
    item = content[0]
    # TextContent tem .text; outros tipos têm representações diferentes
    text = item.text if hasattr(item, "text") else str(item)
    
    if not text:
        raise ValueError(f"Texto vazio no content: {item!r}")
    
    return json.loads(text)


async def main() -> dict:
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": parse_content(criar),
                "listar_resultado": parse_content(listar),
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
