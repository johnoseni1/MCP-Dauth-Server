import asyncio
import json
import os
import sys
from typing import Any, Dict, List
import inspect
from dotenv import load_dotenv


try:
    from main import server
except ImportError:
    try:
        from server import server
    except ImportError:
        print("❌ Could not import 'server' from main.py or server.py")
        sys.exit(1)

load_dotenv()

class InteractiveClient:
    def __init__(self):
        self.tools = self._get_server_tools()
        print(f"✅ Loaded {len(self.tools)} tools from server.")

    def _get_server_tools(self) -> Dict[str, Any]:
        """Extract tool callables from the server instance"""
        tools = {}
        if hasattr(server, 'tools') and hasattr(server.tools, '_tool_specs'):
            for name, spec in server.tools._tool_specs.items():
                if hasattr(spec, 'fn'):
                    tools[name] = spec.fn
        return tools

    def print_menu(self):
        print("\n🔧 Available Tools:")
        tool_names = list(self.tools.keys())
        for i, name in enumerate(tool_names):
            
            fn = self.tools[name]
            doc = inspect.getdoc(fn) or "No description"
            summary = doc.split('\n')[0]
            print(f"  {i+1}. {name} - {summary}")
        print("  q. Quit")

    async def execute_tool(self, tool_name: str):
        fn = self.tools[tool_name]
        sig = inspect.signature(fn)
        
        print(f"\n🛠️  Executing: {tool_name}")
        print(f"   Description: {inspect.getdoc(fn)}")
        print(f"   Arguments: {sig}")

        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'return': continue
            

            is_optional = param.default != inspect.Parameter.empty
            optional_text = "(Optional)" if is_optional else "(Required)"
            default_text = f" [default: {param.default}]" if is_optional else ""
            
            user_input = input(f"   👉 Enter value for '{param_name}' {optional_text}{default_text}: ").strip()
            
            if not user_input and is_optional:
                continue 
            

            try:
                if (param.annotation == dict or param.annotation == Dict or 
                    param.annotation == list or param.annotation == List):
                    value = json.loads(user_input)
                elif param.annotation == int:
                    value = int(user_input)
                elif param.annotation == float:
                    value = float(user_input)
                elif param.annotation == bool:
                    value = user_input.lower() in ('true', '1', 't', 'y', 'yes')
                else:
                    value = user_input
                
                kwargs[param_name] = value
            except json.JSONDecodeError:
                print(f"   ⚠️  Error parsing JSON for {param_name}. Using string '{user_input}'.")
                kwargs[param_name] = user_input
            except ValueError:
                 print(f"   ⚠️  Error converting type for {param_name}. Using original string.")
                 kwargs[param_name] = user_input

        print("\n⏳ Running...")
        try:
            if inspect.iscoroutinefunction(fn):
                result = await fn(**kwargs)
            else:
                result = fn(**kwargs)
            
            print("\n🎉 Result:")
            print(json.dumps(result, indent=2, default=str))
        except Exception as e:
            print(f"\n❌ Error executing tool: {e}")

    async def run(self):
        print("🚀 DAuth MCP Interactive Client")
        print("===============================")
        
        while True:
            self.print_menu()
            choice = input("\n👉 Select a tool (1-N) or 'q': ").strip()
            
            if choice.lower() == 'q':
                print("Bye! 👋")
                break
                
            try:
                idx = int(choice) - 1
                tool_names = list(self.tools.keys())
                if 0 <= idx < len(tool_names):
                    await self.execute_tool(tool_names[idx])
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")

if __name__ == "__main__":
    client = InteractiveClient()
    asyncio.run(client.run())
