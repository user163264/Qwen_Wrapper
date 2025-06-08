#!/usr/bin/env python3
"""
Qwen Filesystem API Integration Script - Version 2
Optimized for LMStudio's Jinja template format and function calling
"""

import json
import sys
import os
from pathlib import Path
from openai import OpenAI

# Add the src directory to Python path so we can import our filesystem handler
sys.path.append(str(Path(__file__).parent))
from filesystem_handler import FilesystemHandler

class QwenFilesystemIntegrationV2:
    def __init__(self, base_url="http://localhost:1234/v1"):
        """Initialize the integration with LMStudio API."""
        self.client = OpenAI(
            base_url=base_url,
            api_key="lm-studio"  # Some versions need a dummy key
        )
        # Let LMStudio determine the model name
        self.model = None  # Will be auto-detected
        self.filesystem_handler = FilesystemHandler()
        
        # OpenAI-compatible function schemas (required by LMStudio)
        self.function_schemas = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the complete contents of a file from the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "The file path to read"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file (creates new or overwrites existing)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "The file path to write to"
                            },
                            "content": {
                                "type": "string", 
                                "description": "The content to write to the file"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List all files and directories in a given path",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "The directory path to list"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_directory",
                    "description": "Create a new directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "The directory path to create"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for files matching a pattern in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "Directory to search in"
                            },
                            "pattern": {
                                "type": "string", 
                                "description": "File pattern to search for"
                            }
                        },
                        "required": ["path", "pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_info",
                    "description": "Get detailed information about a file or directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "Path to get information about"
                            }
                        },
                        "required": ["path"]
                    }
                }
            }
        ]
    
    def auto_detect_model(self):
        """Auto-detect the loaded model in LMStudio"""
        try:
            # Try common model names
            model_attempts = [
                "qwen2.5-coder-1.5b-instruct",
                "Qwen2.5-Coder-1.5B-Instruct",
                "qwen2.5-coder",
                None  # Let OpenAI client auto-detect
            ]
            
            for model_name in model_attempts:
                try:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": "Hi"}],
                        max_tokens=10
                    )
                    self.model = model_name
                    print(f"✅ Detected model: {model_name or 'auto-detected'}")
                    return True
                except:
                    continue
                    
            return False
        except Exception as e:
            print(f"❌ Model detection failed: {e}")
            return False
    
    def execute_function(self, function_name, arguments):
        """Execute a filesystem function and return the result."""
        try:
            # Get the method from filesystem handler
            method = getattr(self.filesystem_handler, function_name)
            
            # Execute the function with arguments
            if arguments:
                result = method(**arguments)
            else:
                result = method()
            
            return result
            
        except AttributeError:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Function execution error: {str(e)}"
            }
    
    def chat_with_filesystem_access(self, user_message, conversation_history=None):
        """
        Send a message to Qwen with filesystem access capabilities.
        Uses simplified approach for better LMStudio compatibility.
        """
        if conversation_history is None:
            conversation_history = []
        
        # Build messages
        messages = conversation_history + [{"role": "user", "content": user_message}]
        
        try:
            # First attempt: Try with tools parameter (OpenAI format)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.function_schemas,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message
            
            # Add assistant response to conversation
            response_dict = {
                "role": "assistant",
                "content": assistant_message.content
            }
            
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                response_dict["tool_calls"] = assistant_message.tool_calls
            
            messages.append(response_dict)
            
            # Check for function calls
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                print(f"\n🔧 Processing {len(assistant_message.tool_calls)} function call(s)...")
                
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"  📁 Calling: {function_name}({function_args})")
                    
                    # Execute function
                    result = self.execute_function(function_name, function_args)
                    
                    # Add tool response
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
                
                # Get final response after tool execution
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1000
                )
                
                final_message = final_response.choices[0].message
                messages.append({
                    "role": "assistant",
                    "content": final_message.content
                })
                
                return {
                    "response": final_message.content,
                    "conversation": messages,
                    "functions_called": len(assistant_message.tool_calls)
                }
            
            else:
                # No function calls detected
                return {
                    "response": assistant_message.content,
                    "conversation": messages,
                    "functions_called": 0
                }
                
        except Exception as e:
            print(f"❌ API Error: {e}")
            
            # Fallback: Try without tools (for debugging)
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1000
                )
                
                return {
                    "response": response.choices[0].message.content,
                    "conversation": messages + [{"role": "assistant", "content": response.choices[0].message.content}],
                    "functions_called": 0,
                    "fallback": True
                }
            except Exception as fallback_error:
                return {
                    "response": f"Connection error: {str(e)}. Fallback error: {str(fallback_error)}",
                    "conversation": messages,
                    "functions_called": 0,
                    "error": True
                }
    
    def test_function_calling_capability(self):
        """Test if function calling is working with current setup"""
        print("🧪 Testing function calling capability...")
        
        test_message = "Please list the files in the current directory using the list_directory function."
        
        result = self.chat_with_filesystem_access(test_message)
        
        if result.get("functions_called", 0) > 0:
            print("🎉 Function calling is working!")
            return True
        elif result.get("fallback"):
            print("⚠️  Function calling not supported, but basic chat works")
            return False
        else:
            print("❌ Function calling not detected")
            return False
    
    def interactive_chat(self):
        """Start an interactive chat session with Qwen."""
        print("🤖 Qwen Filesystem Assistant v2 Ready!")
        
        # Test function calling on startup
        functions_work = self.test_function_calling_capability()
        
        if not functions_work:
            print("\n⚠️  Function calling not working. You can still chat, but no file operations.")
            print("🔧 Try enabling 'Function Calling' or 'Tools' in LMStudio settings.")
        
        print("\n📁 Available directories:", self.filesystem_handler.get_allowed_directories()["allowed_directories"])
        print("💬 Type 'quit' to exit, 'help' for commands\n")
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    conversation_history = []
                    print("🧹 Conversation history cleared!")
                    continue
                    
                if user_input.lower() == 'test':
                    self.test_function_calling_capability()
                    continue
                
                if not user_input:
                    continue
                
                # Get response from Qwen
                result = self.chat_with_filesystem_access(user_input, conversation_history)
                
                # Update conversation history
                conversation_history = result["conversation"]
                
                # Display response with context
                if result.get("functions_called", 0) > 0:
                    print(f"\n🤖 Qwen (executed {result['functions_called']} function(s)): {result['response']}")
                elif result.get("fallback"):
                    print(f"\n🤖 Qwen (no function calling): {result['response']}")
                else:
                    print(f"\n🤖 Qwen: {result['response']}")
                
                if result.get("error"):
                    print("⚠️  Error occurred during conversation.")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show available commands and capabilities."""
        print("\n📖 Qwen Filesystem Assistant v2 Help")
        print("=" * 45)
        print("Commands:")
        print("  help  - Show this help message")
        print("  clear - Clear conversation history")
        print("  test  - Test function calling capability")
        print("  quit  - Exit the assistant")
        print("\nFilesystem Functions Available:")
        print("  📄 read_file(path) - Read file contents")
        print("  📝 write_file(path, content) - Write to file")
        print("  📁 list_directory(path) - List directory contents")
        print("  📂 create_directory(path) - Create directory")
        print("  🔍 search_files(path, pattern) - Search for files")
        print("  ℹ️  get_file_info(path) - Get file information")
        print("\nExample Requests:")
        print("  'Create a Python hello world script'")
        print("  'Show me what files are in this directory'")
        print("  'Read the README.md file'")
        print("  'Make a new folder called test_data'")
        print()

def main():
    """Main entry point for the integration script v2."""
    print("🚀 Starting Qwen Filesystem Integration v2...")
    
    try:
        # Initialize the integration
        integration = QwenFilesystemIntegrationV2()
        
        # Auto-detect model
        if not integration.auto_detect_model():
            print("❌ Could not connect to LMStudio or detect model")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure LMStudio server is running (localhost:1234)")
            print("2. Load a Qwen model in LMStudio")
            print("3. Enable API server in LMStudio")
            return
        
        # Start interactive session
        integration.interactive_chat()
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("\n🔧 Check:")
        print("1. LMStudio running on localhost:1234")
        print("2. Model loaded and API server started")
        print("3. filesystem_handler.py exists")

if __name__ == "__main__":
    main()
