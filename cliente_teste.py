# cliente_teste.py
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def parse_content(result):
    content = result.content
    if not content:
        raise ValueError("Conteúdo vazio na resposta da tool")
    item = content[0]
    text = item.text if hasattr(item, "text") else str(item)
    if not text:
        raise ValueError(f"Texto vazio no content: {item!r}")
    return json.loads(text)


async def main() -> dict:
    params = StdioServerParameters(command="python3", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            criar_resultado = parse_content(criar)
            listar_resultado = parse_content(listar)

            # Garante lista
            if isinstance(listar_resultado, dict):
                listar_resultado = [listar_resultado]

            return {
                "tools": nomes,
                "criar_resultado": criar_resultado,
                "listar_resultado": listar_resultado,
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
