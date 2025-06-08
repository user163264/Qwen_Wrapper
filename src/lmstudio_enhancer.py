#!/usr/bin/env python3
"""
LMStudio Chat Enhancer
Monitors LMStudio responses and executes function calls automatically
"""

import json
import re
import time
import requests
from pathlib import Path
import sys

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))
from filesystem_handler import FilesystemHandler

class LMStudioEnhancer:
    def __init__(self):
        self.filesystem_handler = FilesystemHandler()
        self.lmstudio_api = "http://localhost:1234/v1"
        
    def execute_function(self, function_name, arguments):
        """Execute a filesystem function and return the result."""
        try:
            # Map parameters
            if arguments and 'path' in arguments:
                path_value = arguments['path']
                if function_name in ['read_file', 'write_file']:
                    arguments['file_path'] = path_value
                    del arguments['path']
                elif function_name == 'list_directory':
                    arguments['directory_path'] = path_value
                    del arguments['path']
                elif function_name == 'create_directory':
                    arguments['directory_path'] = path_value
                    del arguments['path']
                elif function_name == 'search_files':
                    arguments['search_path'] = path_value
                    del arguments['path']
            
            method = getattr(self.filesystem_handler, function_name)
            
            if arguments:
                result = method(**arguments)
            else:
                result = method()
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def parse_and_execute_json(self, text):
        """Parse JSON function calls from text and execute them."""
        try:
            # Try to find JSON in the text
            json_pattern = r'\{[^{}]*"tool_calls"[^{}]*\[[^\]]*\][^{}]*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            if matches:
                for match in matches:
                    try:
                        data = json.loads(match)
                        if "tool_calls" in data:
                            print(f"\n🔧 Found function calls in LMStudio response!")
                            for tool_call in data["tool_calls"]:
                                if "function" in tool_call:
                                    func_name = tool_call["function"]["name"]
                                    func_args = tool_call["function"]["arguments"]
                                    print(f"📁 Executing: {func_name}({func_args})")
                                    
                                    result = self.execute_function(func_name, func_args)
                                    
                                    if result.get("success", True):
                                        print(f"✅ Success: {result}")
                                    else:
                                        print(f"❌ Error: {result.get('error')}")
                            return True
                    except json.JSONDecodeError:
                        continue
            
            # If no JSON found, try to parse as direct JSON
            try:
                data = json.loads(text)
                if "tool_calls" in data:
                    # Same execution logic as above
                    return True
            except:
                pass
                
            return False
            
        except Exception as e:
            print(f"Parse error: {e}")
            return False
    
    def interactive_monitor(self):
        """Interactive mode to process LMStudio responses."""
        print("🚀 LMStudio Chat Enhancer Ready!")
        print("📋 Instructions:")
        print("1. Chat normally in LMStudio")
        print("2. When you get a response with function calls, paste it here")
        print("3. The enhancer will execute the functions automatically")
        print("💬 Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("Paste LMStudio response (or type your command): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Try to parse and execute any function calls
                executed = self.parse_and_execute_json(user_input)
                
                if not executed:
                    print("ℹ️  No function calls found in that response.")
                    print("💡 Make sure to paste the full JSON response from LMStudio.")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    enhancer = LMStudioEnhancer()
    enhancer.interactive_monitor()

if __name__ == "__main__":
    main()
